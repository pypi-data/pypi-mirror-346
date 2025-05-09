import logging
from datetime import datetime
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import (
    AnyMessage
)
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent

from veri_agents_playground.agents.providers import LLMProvider, ToolProvider, KnowledgebaseProvider
from veri_agents_playground.agents.workflow import Workflow

log = logging.getLogger(__name__)


class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_messages]
    # retrieved_videos: Annotated[List[dict], operator.add]


class VeritoneSupport(Workflow):
    def __init__(self, name: str, description: str, icon: str, llm: str, **kwargs):
        super().__init__(name=name, description=description, icon=icon, **kwargs)
        self.llm = LLMProvider.get_llm(llm)
        if not self.llm:
            raise ValueError("LLM not found: " + llm)
        support_kb_tool = ToolProvider.get_tool("veritone_support")
        if not support_kb_tool:
            raise ValueError("Tool not found: veritone_support")
        kb = KnowledgebaseProvider.get_knowledgebase("veritone_support")
        if kb is None:
            raise ValueError("Knowledgebase veritone_support not found.")
        products = kb.products # type: ignore
        human_selection_tool = ToolProvider.get_tool("human_selection_fixed_options")
        if not human_selection_tool:
            raise ValueError("Tool not found: human_selection")
        human_selection_tool.description = "Ask the user to select a product to get more information about."
        human_selection_tool.message = "Please select a product:" # pyright: ignore[reportAttributeAccessIssue]
        human_selection_tool.options = list(products) # pyright: ignore[reportAttributeAccessIssue]

        self.tools = [support_kb_tool, human_selection_tool]
        self.system_prompt = f"""You are a helpful support agent answering questions of users about Veritone's products using tools to retrieve the necessary knowledge. If a tool does not give you all the information you need, try again with a different query. If it's not clear which product a question is about, use the 'human_selection_f' tool. Today's date is: {datetime.now().strftime('%Y-%m-%d')}. The Veritone products you can search for are: {', '.join(products)}."""
        self.system_prompt +=  """
             Key Points to Follow:
             - **Strict Answering Rules**: Do not include any unnecessary text. The answer should be concise and focused directly on the question.
             - **Professional Language**: Do not use any abusive or prohibited language. Always respond in a polite and gentle tone.
             - **No Personal Information Requests**: Do not ask for personal information from the user at any point.
             - **Semantic Similarity**: If exact wording is not available in the Context, use your semantic understanding to infer the answer. If there are semantically related phrases, use them to generate a precise response. Use natural language understanding to interpret closely related words or concepts.
             - **Unavailable Information**: If the answer is genuinely not found in the Context, politely apologize and inform the user that the specific information is not available in the provided context.
             Respond in a polite, professional, and concise manner.
        """

        self.workflow = create_react_agent(
            model=self.llm,
            tools=self.tools
        )

    def get_graph(self):
        return self.workflow
