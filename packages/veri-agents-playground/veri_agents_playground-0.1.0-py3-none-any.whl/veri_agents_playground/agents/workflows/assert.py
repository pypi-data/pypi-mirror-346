import asyncio
import logging
from typing import Annotated, List, NotRequired, Optional, Sequence, TypedDict

from langchain_core.language_models import LanguageModelLike

from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.graph.graph import CompiledGraph
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from veri_agents_playground.agents.knowledgebase import Knowledgebase, KnowledgeFilter
from veri_agents_playground.agents.llm import LLMProvider
from veri_agents_playground.agents.workflow import Workflow

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Observation(BaseModel):
    """Observation extracted from a document.
       For example "Officer J. Miller enters the building without a warrant" or "Latch 4 was installed in conductor 1".
    """
    observation: str = Field(
        description="Observation extracted from the document.",
        examples=[
            "Officer J. Miller enters the building without a warrant",
            "Latch 4 was installed in conductor 1",
            "Officer S. Jones pulls his gun.",
        ])
    # TODO: can we get more precise with the sources?
    sources: list[str] = Field(
        description="List of sources for the observation",
        examples=[
            ["police_report.pdf", "incident.pdf"],
        ])


class Assertion(BaseModel):
    """Assertion made by the agent about an observation.
       For example "Observation 'Officer J. Miller enters the building without a warrant' violates policy 'Officer should not enter the building without a warrant'". 
    """
    observation: str = Field(description="Observation the assertion is made about.",)
    policy: str = Field(
        description="Policy the observation is asserted against",
        examples=[
            "Officer should not enter the building without a warrant",
            "Officer should not pull his gun unless in danger",
        ])
    fulfillment: bool = Field(description="Whether the observation fulfills the policy or not")

    # TODO: can we get more precise with the sources?
    sources: list[str] = Field(
        description="List of sources for the assertion",
        examples=[
            ["police_manual.pdf"],
            ["technical_guidelines.pdf"],
        ])


class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_messages]
    observations: list[Observation]
    assertions: list[Assertion]


def create_assert_agent(
    extract_llm: LanguageModelLike,
    assert_llm: LanguageModelLike,
    observations: Knowledgebase,
    policies: Knowledgebase,
    observations_filter: KnowledgeFilter | None = None,
    policies_filter: KnowledgeFilter | None = None,
) -> CompiledGraph:
    """Creates a Veritone Assert agent that extracts observations from a knowledgebase (the observations kb)
       and then asserts them against another knowledgebase (the policies kb).

    Args:
        extract_llm (LanguageModelLike): LLM to use for extraction of individual observations
        assert_llm (LanguageModelLike): LLM to use for assertion/comparison of observations with policies
        observations (Knowledgebase): Knowledgebase to extract from
        policies (Knowledgebase): Knowledgebase to assert against
        observations_filter (KnowledgeFilter | None): Filter for the observations knowledgebase
        policies_filter (KnowledgeFilter | None): Filter for the policies knowledgebase
    """

    def extract_node(agent_state: AgentState, config: RunnableConfig):
       return {} 

    def assert_node(agent_state: AgentState, config: RunnableConfig):
        return {}

    graph = StateGraph(AgentState)
    graph.add_node("extract", extract_node)
    graph.add_node("assert", assert_node)
    graph.add_edge(START, "extract")
    graph.add_edge("extract", "assert")
    graph.add_edge("assert", END)
    return graph.compile()



class Assert(Workflow):

    def __init__(
        self,
        name: str,
        description: str,
        icon: str,
        llm: str,
        system_prompt: str,
        knowledgebase: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            icon=icon,
            #input_schema=ExtractInputSchema,
            #output_schema=ExtractOutputSchema,
            **kwargs,
        )
        self.llm_name = llm
        self.knowledgebase_name = knowledgebase
        self.system_prompt = system_prompt
        self.summarize_prompt = "Summarize your findings about the extracted entities from the documents: \n"
        self.max_concurrent_docs = 3
        self.max_concurrent_chunks = 5
        self.retries_per_chunk = 5
        self.docs_semaphore = asyncio.Semaphore(self.max_concurrent_docs)

        #self.workflow = create_assert_agent(...)



    # async def _invoke_llm(self, llm, messages, retries: int = 3):
    #     """Invoke the LLM with the given messages"""
    #     for _ in range(retries):  # Retry up to 3 times
    #         try:
    #             response = await llm.ainvoke(messages)
    #             return response
    #         # should try to handle more specific exceptions
    #         # but it seems we have to break abstraction here
    #         # for example Nova gives us botocore exceptions
    #         except Exception as e:
    #             log.warning("Extract: error: %s. Retrying...", e)
    #             await asyncio.sleep(3)
    #     raise RuntimeError("LLM invocation failed after %d retries" % retries)

    # async def _chunk_content(self, content: str, max_chunk_length: int) -> list[str]:
    #     """Chunk the document into smaller pieces to fit within the max character length."""
    #     chunks = []
    #     start = 0
    #     while start < len(content):
    #         end = min(start + max_chunk_length, len(content))
    #         # If not at the end of content, try to find a good break point
    #         if end < len(content):
    #             # Try to break at paragraph, sentence, or word boundary
    #             for break_char in ["\n\n", "\n", ". ", " "]:
    #                 potential_end = content.rfind(break_char, start + 1, end)
    #                 if potential_end > start:
    #                     end = potential_end + len(break_char)
    #                     break
    #         chunks.append(content[start:end])
    #         start = end
    #     return chunks

    # async def _process_single_doc(
    #     self,
    #     doc,
    #     messages,
    #     llm_structured,
    #     retries_per_chunk: int = 3,
    #     max_chunk_length: int = 30000,
    # ) -> tuple[str, Entities]:
    #     """Process a document, extracting entities, chunking it if it exceeds the max token length threshold.

    #     Args:
    #         doc: Document to process.
    #         messages: Message history.
    #         llm_structured: LLM with structured output.
    #         retries_per_chunk: Number of retries for each chunk.
    #         max_chunk_length: Maximum length of each chunk.
    #     Returns:
    #         A tuple containing the document source and the extracted entities.
    #     """
    #     async with self.docs_semaphore:
    #         content = doc.page_content
    #         source = doc.metadata["source"]

    #         # If content is short enough, process it in one go
    #         if len(content) <= max_chunk_length:
    #             send_messages = [
    #                 SystemMessage(content=self.system_prompt),
    #                 messages[-1],
    #                 HumanMessage(content=content),
    #             ]
    #             response = await self._invoke_llm(
    #                 llm_structured, send_messages, retries_per_chunk
    #             )
    #             log.debug("Extract: Response for full document: %s", response)
    #             return source, response.entities

    #         # For longer content, chunk it and process each chunk
    #         chunks = await self._chunk_content(content, max_chunk_length)
    #         log.debug(f"Split document into {len(chunks)} chunks")

    #         # Process each chunk and merge results
    #         all_entities: dict[str, list[str]] = {}

    #         for i in range(0, len(chunks), self.max_concurrent_chunks):
    #             chunk_seq = chunks[i : i + self.max_concurrent_chunks]
    #             send_messages = [
    #                 [
    #                     SystemMessage(content=self.system_prompt),
    #                     messages[-1],
    #                     HumanMessage(
    #                         content=f"Provided data: [PART {i + 1}/{len(chunks)}]\\n\\n{chunk}"
    #                     ),
    #                 ]
    #                 for chunk in chunk_seq
    #             ]
    #             results = await asyncio.gather(
    #                 *[
    #                     self._invoke_llm(
    #                         llm_structured, chunk_messages, retries_per_chunk
    #                     )
    #                     for chunk_messages in send_messages
    #                 ]
    #             )
    #             for response in results:
    #                 # Merge entities from this chunk with overall entities
    #                 for entity_type, entities in response.entities.items():
    #                     if entity_type not in all_entities:
    #                         all_entities[entity_type] = []

    #                     # Add only new entities (avoid duplicates)
    #                     for entity in entities:
    #                         if entity not in all_entities[entity_type]:
    #                             all_entities[entity_type].append(entity)

    #         # Remove duplicates from all entities
    #         for entity_type, entities in all_entities.items():
    #             all_entities[entity_type] = list(set(entities))

    #         return source, all_entities

    # async def process_docs(self, docs, messages, llm_structured) -> EntitiesPerDocument:
    #     """Process documents concurrently to extract entities.

    #     Args:
    #         docs: List of documents to process.
    #         messages: Message history.
    #         llm_structured: LLM with structured output.

    #     Returns:
    #         A dictionary mapping document sources to extracted entities.
    #     """
    #     extraction_results: dict[str, dict[str, list[str]]] = {}
    #     results = await asyncio.gather(
    #         *[
    #             self._process_single_doc(
    #                 doc, messages, llm_structured, self.retries_per_chunk
    #             )
    #             for doc in docs
    #         ]
    #     )
    #     for source, entities in results:
    #         extraction_results[source] = entities
    #     return extraction_results

    # def _get_llm_from_config(self, config: RunnableConfig):
    #     """Get the LLM from the config"""
    #     llm_override = Workflow.get_args_from_config(config, "llm")
    #     llm = LLMProvider.get_llm(llm_override or self.llm_name)
    #     if llm is None:
    #         raise ValueError(f"LLM {llm_override} not found.")
    #     return llm

    # def _get_from_config(self, config: RunnableConfig):
    #     """Gets all required parameters from the config."""
    #     kb_override = Workflow.get_args_from_config(config, "knowledgebase")
    #     doc_filter = Workflow.get_args_from_config(config, "documents")
    #     tag_any_filter = Workflow.get_args_from_config(config, "tags_any")
    #     tag_all_filter = Workflow.get_args_from_config(config, "tags_all")
    #     kb = None
    #     if kb_override:
    #         kb = Knowledgebase.get_knowledgebase(kb_override)
    #     elif self.knowledgebase_name:
    #         kb = Knowledgebase.get_knowledgebase(self.knowledgebase_name)
    #     if kb is None:
    #         raise ValueError(f"Knowledgebase {kb_override} not found.")
    #     llm = self._get_llm_from_config(config)
    #     return kb, llm, doc_filter, tag_any_filter, tag_all_filter

    # async def extract(self, state: AgentState, config: RunnableConfig) -> AgentState:
    #     """LangGraph node to extract entities from the documents"""
    #     kb, llm, doc_filter, tag_any_filter, tag_all_filter = self._get_from_config(
    #         config
    #     )
    #     try:
    #         messages = state["messages"]
    #         docs = kb.get_documents(
    #             doc_filter=doc_filter,
    #             tag_any_filter=tag_any_filter,
    #             tag_all_filter=tag_all_filter,
    #         )
    #         llm_structured = llm.with_structured_output(ExtractionResponse)

    #         extraction_results = await self.process_docs(docs, messages, llm_structured)
    #         artifact = {
    #             "type": "json",
    #             "source": "extracted_entities",
    #             "documents": extraction_results,
    #         }
    #         return {
    #             "messages": [
    #                 ToolMessage(
    #                     "Extraction complete.",
    #                     tool_call_id="extract",
    #                     artifact=artifact,
    #                 )
    #             ],
    #             "documents": extraction_results,
    #         }
    #     except Exception as e:
    #         log.error("Error in extract: ", exc_info=True)
    #         return {
    #             "messages": [AIMessage(content="Error in extraction: " + str(e))],
    #             "documents": {},
    #         }

    # async def summarize(self, state: AgentState, config: RunnableConfig) -> AgentState:
    #     """LangGraph node to summarize the extracted entities from previous nodes."""
    #     llm = self._get_llm_from_config(config)
    #     try:
    #         messages = state["messages"]
    #         send_messages = [
    #             SystemMessage(content=self.system_prompt),
    #             messages[-2],  # the user input
    #             HumanMessage(content=self.summarize_prompt + str(state["documents"])),
    #         ]

    #         response = await llm.ainvoke(send_messages)
    #         output = ExtractOutputSchema(
    #             content=response.content,
    #             entities=state["documents"],
    #         )

    #         return {
    #             "messages": [
    #                 AIMessage(
    #                     content=output.model_dump_json(),
    #                 )
    #             ],
    #             "documents": state["documents"],
    #         }
    #     except Exception as e:
    #         log.error("Error in summarize: ", exc_info=True)
    #         output = ExtractOutputSchema(
    #             content="Error in summarization: " + str(e),
    #             entities=state["documents"],
    #         )
    #         return {
    #             "messages": [AIMessage(content=output.model_dump_json())],
    #             "documents": state["documents"],
    #         }

    # def get_graph(self):
    #     return self.workflow
