import json
import logging
from datetime import datetime
from typing import Annotated, Dict, List, NotRequired, Sequence, TypedDict
from concurrent.futures import ThreadPoolExecutor, as_completed

from pydantic import BaseModel, Field
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    AIMessage,
)
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.runnables.config import RunnableConfig

from veri_agents_knowledgebase import Knowledgebase, KnowledgeFilter
from veri_agents_playground.agents.providers import LLMProvider, KnowledgebaseProvider
from veri_agents_playground.agents.workflow import Workflow

log = logging.getLogger(__name__)


class ExtractionResponse(BaseModel):
    """Extracted information from documents"""

    summary: str = Field(
        description="Short summary of the document's contents",
        examples=[
            "This document describes an event that took place at 11:30 on Feb 5, 2025"
        ],
    )
    entities: Dict[str, List[str]] = Field(
        description="Entities extracted from the documents",
        examples=[
            {
                "persons": [
                    "John Doe",
                    "Jane James",
                    "S1 (Construction Superintendent)",
                ],
                "objects": ["excavator", "dog"],
            }
        ],
    )


class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_messages]
    # same as entities field in ExtractionResponse above
    documents: NotRequired[Dict[str, List[str]]]


class Extract(Workflow):
    llm: BaseLanguageModel
    kb: Knowledgebase

    def __init__(
        self,
        name: str,
        description: str,
        icon: str,
        llm: str,
        knowledgebase: str,
        system_prompt: str,
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            icon=icon,
            **kwargs,
        )
        if (llm_model := LLMProvider.get_llm(llm)) is None:
            raise ValueError("LLM not found: " + llm)
        self.llm = llm_model
        if (kb := KnowledgebaseProvider.get_knowledgebase(knowledgebase)) is None:
            raise ValueError(f"Knowledgebase {knowledgebase} not found.")
        self.kb = kb
        self.system_prompt = system_prompt
        self.system_prompt += (
            f"""Today's date is: {datetime.now().strftime("%Y-%m-%d")}."""
        )
        self.summarize_prompt = "Summarize your findings about the extracted entities from the documents: \n"
        # self.system_prompt += """
        #      Key Points to Follow:
        #      - **Strict Answering Rules**: Do not include any unnecessary text. The answer should be concise and focused directly on the question.
        #      - **Professional Language**: Do not use any abusive or prohibited language. Always respond in a polite and gentle tone.
        #      - **No Personal Information Requests**: Do not ask for personal information from the user at any point.
        #      - **Semantic Similarity**: If exact wording is not available in the Context, use your semantic understanding to infer the answer. If there are semantically related phrases, use them to generate a precise response. Use natural language understanding to interpret closely related words or concepts.
        #      - **Unavailable Information**: If the answer is genuinely not found in the Context, politely apologize and inform the user that the specific information is not available in the provided context.
        #      Respond in a polite, professional, and concise manner.
        # """
        # - **Concise & Understandable**: Provide the most concise, clear, and understandable answer possible.
        # - **Precise Answer Length**: The answer must be between a minimum of 40 words and a maximum of 100 words.
        # prompt = ChatPromptTemplate.from_template(template)

        # build graph
        workflow = StateGraph(AgentState)
        workflow.add_node("extract", self.extract)
        workflow.add_node("summarize", self.summarize)
        workflow.add_edge(START, "extract")
        workflow.add_edge("extract", "summarize")
        workflow.add_edge("summarize", END)
        self.workflow = workflow.compile()

    def _process_single_doc(
        self, doc, messages, llm_structured
    ) -> tuple[str, List[str]]:
        send_messages = [
            SystemMessage(content=self.system_prompt),
            messages[-1],
            HumanMessage(content=doc.page_content),
        ]
        response = llm_structured.invoke(send_messages)
        return doc.metadata["source"], response.entities

    def process_docs(self, docs, messages, llm_structured):
        extraction_results: Dict[str, List[str]] = {}

        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks
            future_to_doc = {
                executor.submit(
                    self._process_single_doc, doc, messages, llm_structured
                ): doc
                for doc in docs
            }

            # Collect results as they complete
            for future in as_completed(future_to_doc):
                source, entities = future.result()
                extraction_results[source] = entities

        return extraction_results

    def extract(self, state: AgentState, config: RunnableConfig) -> AgentState:
        """Extract entities from the documents"""
        try:
            messages = state["messages"]

            kb_override = Workflow.get_args_from_config(config, "knowledgebase")
            doc_filter = Workflow.get_args_from_config(config, "documents")
            tag_filter = Workflow.get_args_from_config(config, "tags")

            if kb_override:
                kb = KnowledgebaseProvider.get_knowledgebase(kb_override)
                if kb is None:
                    return {
                        "messages": [
                            AIMessage(content=f"Knowledgebase {kb_override} not found.")
                        ]
                    }
            else:
                kb = self.kb
            docs = kb.get_documents(
                KnowledgeFilter(docs=doc_filter, tags_any_of=tag_filter)
            )
            llm_structured = self.llm.with_structured_output(ExtractionResponse)

            extraction_results = self.process_docs(docs, messages, llm_structured)
            artifact = {
                "type": "json",
                "source": "extracted_entities",
                "documents": extraction_results,
            }
            return {
                "messages": [
                    ToolMessage(
                        "Extraction complete.",
                        tool_call_id="extract",
                        artifact=artifact,
                    )
                ],
                "documents": extraction_results,
            }
        except Exception as e:
            log.error("Error in extract: ", exc_info=True)

            return {"messages": [AIMessage(content="Error in extraction: " + str(e))]}

    def summarize(self, state: AgentState) -> AgentState:
        """Summarize the extracted entities"""
        try:
            messages = state["messages"]
            send_messages = [
                SystemMessage(content=self.system_prompt),
                messages[-2],  # the user input
                HumanMessage(
                    content=self.summarize_prompt + str(state["documents"]) # pyright: ignore[reportTypedDictNotRequiredAccess]
                ),
            ]

            # llm_structured = self.llm.with_structured_output(SummaryResponse)
            # response = llm_structured.invoke(send_messages)

            response = self.llm.invoke(send_messages)

            return {"messages": [AIMessage(json.dumps({
                "summary": response.content,
                "documents": state["documents"], # pyright: ignore[reportTypedDictNotRequiredAccess]
            }))]}
        except Exception as e:
            log.error("Error in summarize: ", exc_info=True)
            return {
                "messages": [AIMessage(content="Error in summarization: " + str(e))]
            }

    def get_graph(self):
        return self.workflow
