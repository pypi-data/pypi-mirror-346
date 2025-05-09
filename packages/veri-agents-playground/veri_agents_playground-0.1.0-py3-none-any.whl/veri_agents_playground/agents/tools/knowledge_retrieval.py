import logging
from typing import Optional, Tuple, Type

from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from langchain_core.runnables.config import RunnableConfig
from typing_extensions import Annotated
from langgraph.prebuilt import InjectedState
from pydantic import BaseModel, Field

from veri_agents_knowledgebase import Knowledgebase, KnowledgeFilter

log = logging.getLogger(__name__)


class FixedKnowledgebaseQueryInput(BaseModel):
    query: str = Field(
        description="query to search for documents in the knowledgebase."
    )


class FixedKnowledgebaseQuery(BaseTool):
    """Search for documents in a knowledgebase that is not selected by the agent.
    IMPORTANT: The knowledgebase must be specified when initiating through ToolProvider.
    Example:
    ```
    kb_tool = ToolProvider.get_tool("knowledge_retrieval_fixed_kb", knowledgebase="regulations")
    ```
    """

    name: str = "knowledge_retrieval_fixed_kb"
    description: str = (
        "Searches for documents in a knowledgebase. Input should be a search query."
    )
    args_schema: Type[BaseModel] = FixedKnowledgebaseQueryInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    num_results: int = 4
    knowledgebase: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "kb_retrieve_" + self.knowledgebase
        if not self.knowledgebase:
            raise ToolException(
                "Knowledgebase not specified (pass into get_tool as knowledgebase='kb')."
            )
        kb = Knowledgebase.get_knowledgebase(self.knowledgebase)
        if not kb:
            raise ToolException(f"Knowledgebase {self.knowledgebase} not found.")
        self.description = f"Searches for documents in the {kb.name} knowledgebase. Use this tool if you're interested in documents about {kb.description}."

    def _run(
        self,
        query: str,
        # knowledgebase: Annotated[str, InjectedState("knowledgebase")],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[list[str], dict]:
        kb = Knowledgebase.get_knowledgebase(self.knowledgebase)
        if not kb:
            raise ToolException(f"Knowledgebase {self.knowledgebase} not found.")
        log.info(f"Searching in knowledgebase {self.knowledgebase} for {query}")
        docs = kb.retrieve(query, limit=self.num_results)
        log.info(f"Retrieved {len(docs)} documents.")
        # TODO: do we really want all that docling stuff? or filter already during ingestion?
        return [d.page_content for d in docs], {
            "items": docs,
            "type": "document",
            "source": "knowledgebase",
        }


class KnowledgebaseQueryInput(BaseModel):
    query: str = Field(
        description="query to search for documents in the knowledgebase."
    )
    knowledgebase: str = Field(
        "knowledgebase", description="Which knowledgebase to search in."
    )


class KnowledgebaseQuery(BaseTool):
    name: str = "knowledge_retrieval"
    description: str = (
        "Searches for documents in a knowledgebase. Input should be a search query."
    )
    args_schema: Type[BaseModel] = KnowledgebaseQueryInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    num_results: int = 4

    def _run(
        self,
        query: str,
        knowledgebase: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[list[str], dict]:
        kb = Knowledgebase.get_knowledgebase(knowledgebase)
        if not kb:
            raise ToolException(f"Knowledgebase {knowledgebase} not found.")
        self.description = f"Searches for documents in the {kb.name} knowledgebase. Use this tool if you're interested in documents about {kb.description}."
        docs = kb.retrieve(query, limit=self.num_results)
        return [d.page_content for d in docs], {
            "items": docs,
            "type": "document",
            "source": "knowledgebase",
        }


class FixedKnowledgebaseWithTagsQueryInput(BaseModel):
    query: str = Field(
        description="query to search for documents in the knowledgebase."
    )
    tag_any_filters: Optional[list[str]] = Field(
        default=None,
        description="Documents are selected if they match any of the tags in this list. Useful if for example searching for a document that's either about 'electricity' or about 'software'.",
    )
    tag_all_filters: Optional[list[str]] = Field(
        default=None,
        description="Documents are selected if they match all of the tags in this list. Useful if for example searching for a document that's both a 'policy' and valid in 'Nashville'.",
    )


class FixedKnowledgebaseWithTagsQuery(BaseTool):
    """Search for documents in a knowledgebase that is not selected by the agent.
    IMPORTANT: The knowledgebase must be specified when initiating through ToolProvider.
    Example:
    ```
    kb_tool = ToolProvider.get_tool("knowledge_retrieval_fixed_kb_tags", knowledgebase="regulations")
    ```
    """

    name: str = "retrieval_fixkb_tags"
    description: str = "Searches for documents in a knowledgebase. Input should be a search query and optionally tags."
    args_schema: Type[BaseModel] = FixedKnowledgebaseWithTagsQueryInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    num_results: int = 5
    knowledgebase: Knowledgebase

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.name = "kb_retrieve_tags_" + self.knowledgebase.name
        kb_tags = self.knowledgebase.tags
        log.info("Tags: " + str(kb_tags))
        self.description = f"Searches for documents in the {self.knowledgebase.name} knowledgebase. Use this tool if you're interested in documents about {self.knowledgebase.description}."
        if kb_tags:
            self.description += " The knowledgebase has the following tags: "
            for k, v in kb_tags.items():
                self.description += f"{k}: {v}, "

    def _run(
        self,
        query: str,
        config: RunnableConfig,
        tag_any_filters: Optional[list[str]] = None,
        tag_all_filters: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[list[str], dict]:
        # TODO: we somehow have to configure this, what if config wants to have multiple filters for multiple KBs?
        documents_filter = (
            config.get("configurable", {}).get("args", {}).get("documents")
        )
        # if documents filter is given by the caller, ignore tag filters generated by the agent
        if documents_filter:
            tag_any_filters = None
            tag_all_filters = None

        filter = KnowledgeFilter(
            docs=documents_filter,
            tags_any_of=tag_any_filters,
            tags_all_of=tag_all_filters,
        )

        log.info(
            f"[FixedKnowledgebaseWithTagsQuery] Searching in knowledgebase {self.knowledgebase.name} for {query} using filter {filter}"
        )
        docs = self.knowledgebase.retrieve(query, limit=self.num_results, filter=filter)
        log.info(f"[FixedKnowledgebaseWithTagsQuery] Retrieved {len(docs)} documents.")
        # TODO: do we really want all that docling stuff? or filter already during ingestion?
        return [d.page_content for d in docs] if len(docs) > 0 else [
            "No documents found."
        ], {
            "items": docs,
            "type": "document",
            "source": "knowledgebase",
        }


class FixedKnowledgebaseListDocumentsInput(BaseModel):
    tag_any_filters: Optional[list[str]] = Field(
        default=None,
        description="Documents are selected if they match any of the tags in this list. Useful if for example searching for a document that's either about 'electricity' or about 'software'.",
    )
    tag_all_filters: Optional[list[str]] = Field(
        default=None,
        description="Documents are selected if they match all of the tags in this list. Useful if for example searching for a document that's both a 'policy' and valid in 'Nashville'.",
    )


class FixedKnowledgebaseListDocuments(BaseTool):
    """List documents in a knowledgebase that is not selected by the agent.
    IMPORTANT: The knowledgebase must be specified when initiating through ToolProvider or constructor.
    Example:
    ```
    kb_tool = ToolProvider.get_tool("knowledge_retrieval_fixed_kb_tags", knowledgebase="regulations")
    ```

    ```
    kb_tool = FixedKnowledgebaseListDocuments(knowledgebase="regulations")
    ```
    """

    name: str = "list_documents"
    description: str = "Lists documents in a knowledgebase"
    args_schema: Type[BaseModel] = FixedKnowledgebaseListDocumentsInput
    #response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    knowledgebase: Knowledgebase

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.name = "kb_list_docs_" + self.knowledgebase.name
        kb_tags = self.knowledgebase.tags
        self.description = f"Lists the documents in the {self.knowledgebase.name} knowledgebase."
        if kb_tags:
            self.description += " The knowledgebase has the following tags: "
            for k, v in kb_tags.items():
                self.description += f"{k}: {v}, "

    def _run(
        self,
        config: RunnableConfig,
        tag_any_filters: Optional[list[str]] = None,
        tag_all_filters: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:  # -> Tuple[list[str], dict]:
        # TODO: would be interesting to not get the content as well
        log.debug("[FixedKnowledgebaseListDocuments] Listing documents")
        docs = self.knowledgebase.get_documents(
            KnowledgeFilter(
                docs=None,
                tags_any_of=tag_any_filters,
                tags_all_of=tag_all_filters,
            )
        )
        log.debug("[FixedKnowledgebaseListDocuments] Retrieved documents.")
        return str([
            (
                d.metadata.get("source"),
                d.metadata.get("doc_name"),
                d.metadata.get("last_updated"),
                d.metadata.get("tags"),
                d.metadata.get("summary"),
            )
            for d in docs
        ])
