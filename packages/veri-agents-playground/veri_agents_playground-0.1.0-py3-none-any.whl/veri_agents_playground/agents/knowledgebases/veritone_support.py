import csv
import logging
from datetime import datetime
from typing import Any, Iterator, List, Optional

from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, Filter, VectorParams
from veri_agents_knowledgebase import DocumentLoader, Knowledgebase, KnowledgeFilter, DataSource
from veri_agents_knowledgebase.qdrant import QdrantDocStore, SourceDocumentRetriever

from veri_agents_playground.agents.providers import LLMProvider

log = logging.getLogger(__name__)


class SupportDocumentLoader(DocumentLoader):
    def __init__(self, data_source: DataSource):
        super().__init__()
        self.data_source = data_source

        self.product_name_map = {
            "aiWare - aiWare": "aiWare",
            "aiWare - Automate Studio": "Automate",
            "Contact App": "Contact",
            "GLC - Redaction Managed Service (RMS)": "Redact",
        }
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=200
        )

    def _parse_html(self, text: str):
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def _split(self, text: str, metadata: dict):
        doc = Document(page_content=text, metadata=metadata)
        new_docs = self.splitter.split_documents([doc])
        return new_docs

    def _add(
        self,
        parent_doc: Document,
        docs: List[Document],
        text: str,
        fieldname: str | None,
        metadata: dict,
    ):
        if text:
            if fieldname:
                parent_doc.page_content += f"{fieldname}: {text}\n"
            else:
                parent_doc.page_content += f"{text}\n"
            new_docs = self._split(text, metadata)
            docs.extend(new_docs)

    def load_documents(self, **kwargs):
        products_to_include = []

        if "products" in kwargs:
            products_to_include = kwargs["products"]
        with open(self.data_source.location, newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            _ = next(csvreader)  # drop the header

            for row in csvreader:
                # unpack the row
                (
                    knowledgearticle_id,
                    title,
                    summary,
                    content,
                    problem,
                    cause,
                    solution,
                    link,
                    product_sequence,
                    question,
                    answer,
                    description,
                    instruction,
                    release_notes,
                ) = row

                if not (
                    summary
                    or content
                    or problem
                    or cause
                    or solution
                    or question
                    or answer
                    or description
                    or instruction
                    or release_notes
                ):
                    continue
                # assuming those fields can hold HTML
                summary = self._parse_html(summary) if summary else ""
                content = self._parse_html(content) if content else ""
                problem = self._parse_html(problem) if problem else ""
                cause = self._parse_html(cause) if cause else ""
                solution = self._parse_html(solution) if solution else ""
                question = self._parse_html(question) if question else ""
                answer = self._parse_html(answer) if answer else ""
                description = self._parse_html(description) if description else ""
                instruction = self._parse_html(instruction) if instruction else ""
                release_notes = self._parse_html(release_notes) if release_notes else ""

                # if the article is related to multiple products
                # TODO: can we use a metadata filter that can handle this
                product_list = product_sequence.split(";")
                for product in product_list:
                    if not product:
                        continue
                    product = self.product_name_map.get(product, product)
                    if product not in products_to_include:
                        continue

                    docs = []
                    metadata = {
                        "source": f"{knowledgearticle_id}_{product}",
                        "title": title,
                        "product": product,
                        "link": link,
                        "last_updated": datetime.now().isoformat(),
                    }
                    # Title as a separate document because we want to use ParentRetriever
                    parent_doc = Document(page_content="", metadata=metadata)
                    self._add(parent_doc, docs, title, "Title", metadata)
                    self._add(parent_doc, docs, summary, "Summary", metadata)
                    self._add(parent_doc, docs, problem, "Problem", metadata)
                    self._add(parent_doc, docs, cause, "Cause", metadata)
                    self._add(parent_doc, docs, solution, "Solution", metadata)
                    self._add(parent_doc, docs, question, "Question", metadata)
                    self._add(parent_doc, docs, answer, "Answer", metadata)
                    self._add(parent_doc, docs, description, "Description", metadata)
                    self._add(parent_doc, docs, instruction, "Instruction", metadata)
                    self._add(
                        parent_doc, docs, release_notes, "Release Notes", metadata
                    )
                    self._add(parent_doc, docs, content, None, metadata)
                    yield parent_doc, docs


class VeritoneSupportKnowledgebase(Knowledgebase):
    def __init__(
        self,
        vectordb_url: str,
        products: List[str],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.llm = kwargs.get("llm")
        self.embedding_model = kwargs.get("embedding_model")
        self.products = products
        self.chunks_collection_name = "chunks_veritone_support"
        self.docs_collection_name = "docs_support_docs"
        self.records_namespace = f"qdrant/{self.chunks_collection_name}"
        self.docs_namespace = f"qdrant/{self.docs_collection_name}"
        self.data_sources = [DataSource.model_validate(d) for d in self.metadata.data_sources]

        self.embedder = LLMProvider.get_llm(self.embedding_model)
        if self.embedder is None:
            raise ValueError("Embedding model not found: " + self.embedding_model)
        self.qdrant = QdrantClient(vectordb_url)
        if not self.qdrant.collection_exists(self.chunks_collection_name):
            self.qdrant.create_collection(
                self.chunks_collection_name,
                vectors_config={
                    "dense": VectorParams(
                        size=1024, distance=Distance.COSINE
                    )  # TODO get size from somewhere
                },
                sparse_vectors_config={
                    "sparse": models.SparseVectorParams(),
                },
            )
        sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
        self.vector_store = QdrantVectorStore(
            client=self.qdrant,
            collection_name=self.chunks_collection_name,
            embedding=self.embedder, # pyright: ignore[reportArgumentType]
            retrieval_mode=RetrievalMode.HYBRID,
            vector_name="dense",
            sparse_embedding=sparse_embeddings,
            sparse_vector_name="sparse",
        )
        self.doc_store = QdrantDocStore(
            client=self.qdrant, collection_name=self.docs_collection_name
        )
        self.doc_store.create_schema()

    def index(self, data_source: Optional[DataSource] = None):
        """Do an index run on either a provides data source or data sources defined in its config.

        Args:
            data_source (DataSource): Data source to index. If None, will use the data sources defined in the config.
        """
        data_sources = [data_source] if data_source else self.data_sources
        for ds in data_sources:
            self._index(ds)

    def _index(self, data_source: DataSource):
        """Do an index run on a data source."""
        # At this point we just consume a CSV from Snowflake, replace with direct Snowflake access at some point

        loader = SupportDocumentLoader(data_source)
        docs = loader.load_documents(products=self.products)

        retriever = SourceDocumentRetriever(
            parent_splitter=None,
            id_key="source",
            vectorstore=self.vector_store,
            docstore=self.doc_store,
        )

        # one yield is one article consisting fo multiple documents
        for parent_doc, child_docs in docs:
            if not parent_doc or not child_docs:
                continue

            # retrieve existing document and compare
            parent_doc_id = parent_doc.metadata["source"]
            existing_docs = self.doc_store.mget([parent_doc_id])
            if len(existing_docs) > 0:
                existing_doc = existing_docs[0]
                # TODO: shall we store hashes or use timestamps?
                # Once we start ingesting images we should probably do this check
                # in parsedocs already :(
                if (
                    data_source.incremental
                    and existing_doc
                    and existing_doc.page_content == parent_doc.page_content
                ):
                    log.info(f"Document {parent_doc_id} already indexed, skipping")
                    continue
                else:
                    log.info(f"Document {parent_doc_id} changed, deleting old data")
                    # unfortunately the langchain abstraction can't do a filtered deleted
                    result = self.qdrant.delete(
                        self.chunks_collection_name,
                        points_selector=models.FilterSelector(
                            filter=models.Filter(
                                must=[
                                    models.FieldCondition(
                                        key="metadata.source",
                                        match=models.MatchValue(value=parent_doc_id),
                                    )
                                ]
                            )
                        ),
                        wait=True,
                    )
                    log.info(f"Deleting {parent_doc_id}  children result: {result}")
                    # chunks deleted, now delete the doc itself
                    self.doc_store.mdelete([parent_doc_id])

            log.info(f"Indexing document {parent_doc_id}")
            retriever.add_documents(parent_doc, child_docs)

    def retrieve(self, query: str, limit: int, **kwargs): # pyright: ignore[reportIncompatibleMethodOverride]
        search_kwargs: dict[str, Any] = {
            "k": limit
            * 10,  # more chunks as multiple chunks might be part of the same doc
        }
        if "product" in kwargs:
            product = str(kwargs["product"])
            search_kwargs["filter"] = Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.product", match=models.MatchValue(value=product)
                    )
                ]
            )
        retriever = SourceDocumentRetriever(
            parent_splitter=None,
            id_key="source",
            vectorstore=self.vector_store,
            docstore=self.doc_store,
            search_kwargs=search_kwargs,
        )
        # TODO: some mechanism to aggregate subdocs scores to parent doc scores, then pick best parents
        return retriever.invoke(query)[:limit]

    def get_documents(
        self,
        filter: KnowledgeFilter | None = None,
    ) -> Iterator[Document]:
        # filter = self._create_filter(doc_filter, tag_filter)
        return self.doc_store.yield_documents(filter=None)
