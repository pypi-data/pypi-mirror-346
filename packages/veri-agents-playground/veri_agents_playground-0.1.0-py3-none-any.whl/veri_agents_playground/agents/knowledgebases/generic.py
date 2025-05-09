from datetime import datetime
import logging
from pathlib import Path
from typing import Callable, Iterator, List, Optional, cast


from langchain_core.language_models import BaseLanguageModel
from langchain_core.embeddings.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models
from qdrant_client.models import Distance, Filter, VectorParams
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling.document_converter import DocumentConverter

from veri_agents_knowledgebase.knowledgebase import DocumentLoader, DataSource, Knowledgebase, KnowledgeFilter
from veri_agents_knowledgebase.qdrant.qdrant_doc_store import QdrantDocStore
from veri_agents_knowledgebase.qdrant.source_retriever import SourceDocumentRetriever
from veri_agents_knowledgebase.qdrant.summarization import Summarizer

log = logging.getLogger(__name__)


class GenericDocumentLoader(DocumentLoader):
    def __init__(self, data_source: DataSource):
        """Generic document loader that loads documents from a location."""
        super().__init__()
        self.data_source = data_source

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=200
        )
        self.embed_model_id = (
            "sentence-transformers/all-MiniLM-L6-v2"  # TODO: change this
        )
        self.chunker = HybridChunker(tokenizer=self.embed_model_id)

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
        files = [
            str(file)
            for file in Path(self.data_source.location).rglob("*")
            if file.is_file()
        ]

        doc_converter = DocumentConverter()

        for f in files:
            log.info(f"Processing {f}")
            parent_result = doc_converter.convert(source=f)

            doc_name = Path(f).name
            doc_location = Path(f).relative_to(self.data_source.location).parent
            parent_doc = Document(
                page_content=parent_result.document.export_to_markdown(
                    image_placeholder=""
                ),
                metadata={
                    "source": f"{self.data_source.name}::{doc_name}::{doc_location}",
                    "data_source": self.data_source.name,
                    "doc_name": doc_name,
                    "doc_location": doc_location,
                    "last_updated": datetime.now().isoformat(),
                    "tags": self.data_source.tags,
                },
            )
            chunk_iter = self.chunker.chunk(parent_result.document)
            child_docs = [
                Document(
                    page_content=self.chunker.serialize(chunk=chunk),
                    metadata={
                        **chunk.meta.export_json_dict(),
                        "data_source": self.data_source.name,
                        "tags": self.data_source.tags,
                    },
                )
                for chunk in chunk_iter
            ]
            yield parent_doc, child_docs


class GenericKnowledgebase(Knowledgebase):
    """A generic knowledgebase that can be used to index and retrieve documents
    from various sources."""

    def __init__(
        self,
        vectordb_url: str,
        llm: BaseLanguageModel | str,
        embedding_model: Embeddings | str,
        #llm_provider: Callable[[str], BaseLanguageModel | Embeddings | None] | None = None,
        #embedding_provider: Callable[[str], Embeddings | None] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.chunks_collection_name = f"chunks_{self.metadata.collection}"
        self.docs_collection_name = f"docs_{self.metadata.collection}"
        self.doc_summarize = self.metadata.doc_summarize
        self.doc_autotag = self.metadata.doc_autotag
        self.data_sources = [
            DataSource.model_validate(d) for d in self.metadata.data_sources
        ]
        self.id_key = "source"  # key to use for the document ID in the docstore
        # self.records_namespace = f"qdrant/{self.chunks_collection_name}"
        # self.docs_namespace = f"qdrant/{self.docs_collection_name}"

        if isinstance(embedding_model, str):
            #FIXME
            from veri_agents_playground.agents.providers import LLMProvider
            self.embedder = cast(Embeddings, LLMProvider.get_llm(embedding_model))
            if self.embedder is None:
                raise ValueError(
                    "Embedding model not found: " + embedding_model
                )
        else:
            self.embedder = embedding_model
        if isinstance(llm, str):
            #FIXME
            from veri_agents_playground.agents.providers import LLMProvider
            self.llm = LLMProvider.get_llm(llm)
            if self.doc_summarize:
                if self.llm is None:
                    raise ValueError(
                        f"llm required for summarization, can't load {llm}"
                    )
                self.summarizer = Summarizer(
                    self.llm,
                    summarize=self.doc_summarize,
                    tags=self.metadata.tags if self.doc_autotag else None,
                )
        else:
            self.llm = llm

        self.qdrant = QdrantClient(vectordb_url)
        log.info(f"Connecting to Qdrant at {vectordb_url}")
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
        log.info(f"Connecting to Qdrant at {vectordb_url} done")
        sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
        self.vector_store = QdrantVectorStore(
            client=self.qdrant,
            collection_name=self.chunks_collection_name,
            embedding=self.embedder,
            retrieval_mode=RetrievalMode.HYBRID,
            vector_name="dense",
            sparse_embedding=sparse_embeddings,
            sparse_vector_name="sparse",
        )
        self.doc_store = QdrantDocStore(
            client=self.qdrant, collection_name=self.docs_collection_name
        )
        self.doc_store.create_schema()

    def process_doc(self, parent_doc: Document, child_docs: List[Document]):
        """Process a document before indexing, this includes summarization and potential other steps."""
        if self.doc_summarize or self.doc_autotag:
            summary, tags = self.summarizer(
                f"Document: {parent_doc.metadata['source']}\nContent: {parent_doc.page_content}\nUser tags: {', '.join(parent_doc.metadata['tags'])}\n"
            )
            parent_doc.metadata["summary"] = summary
            if tags:
                log.debug(f"Predicted tags for {parent_doc.metadata['source']}: {tags}")
                current = set(parent_doc.metadata["tags"])
                current.update(tags)
                parent_doc.metadata["tags"] = list(current)
                for cd in child_docs:
                    cd.metadata["tags"] = list(current)
            log.info(
                f"Summarized {parent_doc.metadata['source']} to {summary}, set tags to {parent_doc.metadata['tags']}"
            )

    def index(self, data_source: Optional[DataSource] = None):
        """Do an index run on either a provides data source or data sources defined in its config.

        Args:
            data_source (DataSource): Data source to index. If None, will use the data sources defined in the config.
        """
        data_sources = [data_source] if data_source else self.data_sources
        for ds in data_sources:
            self._index(ds)

    def _index(self, data_source: DataSource):
        log.info(f"Indexing {data_source.name} ({data_source.location})")
        loader = GenericDocumentLoader(data_source)
        docs = loader.load_documents()

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

                    # unfortunately the langchain abstraction can't do a filtered delete
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

            # additional processing like summarization we only do if the doc changed
            log.info(f"Processing document {parent_doc_id}")
            self.process_doc(parent_doc, child_docs)

            log.info(f"Indexing document {parent_doc_id}")

            # add the documents to the stores
            for doc in child_docs:
                doc.metadata[self.id_key] = parent_doc.metadata[self.id_key]
            self.vector_store.add_documents(child_docs)
            self.doc_store.mset([(parent_doc.metadata[self.id_key], parent_doc)])

    def retrieve(
        self,
        query: str,
        limit: int,
        filter: KnowledgeFilter | None = None,
        **kwargs,
    ):
        # for now let's do naive retrieval
        qdrant_filter = self._create_qdrant_filter(filter)
        log.info(f"Qdrant Filter: {qdrant_filter}")
        return self.vector_store.similarity_search(query, k=limit, filter=qdrant_filter)

    def get_documents(
        self,
        filter: KnowledgeFilter | None = None,
    ) -> Iterator[Document]:
        qdrant_filter = self._create_qdrant_filter(filter)
        return self.doc_store.yield_documents(filter=qdrant_filter)

    def _create_qdrant_filter(
        self,
        filter: KnowledgeFilter | None = None,
    ):
        """Create a Qdrant filter from the knowledgebase filter.
        Args:
            filter (KnowledgeFilter): The knowledge filter to convert.
        Returns:
            Filter: The Qdrant filter.
        """
        if not filter:
            return None

        must = []
        # doc filter means all the documents in the list (so a should clause)
        if filter.docs:
            doc_filter = filter.docs
            if isinstance(filter.docs, str):
                doc_filter = [filter.docs]
            should = []
            for doc_id in doc_filter:
                should.append(
                    models.FieldCondition(
                        key="metadata.source", match=models.MatchValue(value=doc_id)
                    )
                )
            must.append(Filter(should=should))
        if filter.tags_any_of:
            tag_any_filter = filter.tags_any_of
            if isinstance(filter.tags_any_of, str):
                tag_any_filter = [filter.tags_any_of]
            should = []
            for tag in tag_any_filter:
                should.append(
                    models.FieldCondition(
                        key="metadata.tags",
                        match=models.MatchValue(value=tag),
                    )
                )
            must.append(Filter(should=should))
        if filter.tags_all_of:
            tag_all_filter = filter.tags_all_of
            if isinstance(filter.tags_all_of, str):
                tag_all_filter = [filter.tags_all_of]
            for tag in tag_all_filter:
                must.append(
                    models.FieldCondition(
                        key="metadata.tags",
                        match=models.MatchValue(value=tag),
                    )
                )
        return Filter(must=must) if must else None

    def set_tags(
        self,
        doc_id: str,
        tags: list[str],
    ):
        """Sets tags for a document."""
        self.qdrant.set_payload(
            collection_name=self.chunks_collection_name,
            points=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.source",
                        match=models.MatchValue(value=doc_id),
                    )
                ]
            ),
            payload={"tags": tags},
            key="metadata",
            wait=False,
        )

        self.qdrant.set_payload(
            collection_name=self.docs_collection_name,
            points=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.source",
                        match=models.MatchValue(value=doc_id),
                    )
                ]
            ),
            payload={"tags": tags},
            key="metadata",
            wait=False,
        )
