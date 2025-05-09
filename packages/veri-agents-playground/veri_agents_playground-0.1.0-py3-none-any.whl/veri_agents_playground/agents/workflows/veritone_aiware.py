import logging
from datetime import datetime
from typing import Annotated, List, Sequence, TypedDict, cast

from veri_agents_playground.agents.providers import LLMProvider, ToolProvider, KnowledgebaseProvider
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage, BaseMessage
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.language_models.chat_models import BaseChatModel

from veri_agents_playground.agents.workflow import Workflow

log = logging.getLogger(__name__)


class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_messages]


def get_tools(tool_names: list[str]) -> List[BaseTool]:
    tools = []
    for tool_name in tool_names:
        tool = ToolProvider.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found.")
        tools.append(tool)
    return tools


class VeritoneAiWareAgent(Workflow):
    def __init__(
        self, name: str, workspace: str, description: str, icon: str, llm: str, **kwargs
    ):
        super().__init__(
            name=name, workspace=workspace, description=description, icon=icon, **kwargs
        )
        self.cache: dict = {}
        self.history_window = 5  # number of messages to keep in history when talking to the LLM

        # LLM
        self.llm = cast(BaseChatModel, LLMProvider.get_llm(llm))
        if not self.llm:
            raise ValueError("LLM not found: " + llm)

        # Knowledge
        #kb = KnowledgebaseProvider.get_knowledgebase("veritone_support")
        #if kb is None:
        #    raise ValueError("Knowledgebase veritone_support not found.")
        #products = kb.products  # type: ignore

        # Tools
        #human_selection_tool = ToolProvider.get_tool(
        #    "human_selection_fixed_options",
        #    description="Ask the user to select a product to get more information about.",
        #    message="Please select a product:",
        #    options=list(products),
        #)
        #if not human_selection_tool:
        #    raise ValueError("Tool not found: human_selection")
        other_tools = get_tools(
            [
                "aiware_tdos_created_during",
                "aiware_create_tdo_with_asset",
                "aiware_tool",
                "aiware_schema_tool",
            ]
        )
        self.tools = [
            #human_selection_tool,
            *other_tools,
        ]
        self.tool_node = ToolNode(self.tools)
        self.llm = self.llm.bind_tools(self.tools)

        # Prompts
        self.system_prompt = """You are an expert agent assisting with Veritone's aiWARE GraphQL API.
        You can use the aiware_ tools to access the aiWARE API to work with TDOs, SDOs, and other aiWARE resources.  """

        # Workflow
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("action", self.call_tool)
        workflow.add_edge(START, "agent")

        # no additional tools to call? End
        workflow.add_conditional_edges(
            "agent",
            self.agent_done,
            {
                "continue": "action",
                "end": END,
            },
        )

        # if we asked the human something we have to go to end and wait for an answer
        workflow.add_conditional_edges(
            "action",
            self.wait_for_human,
            {
                "continue": "agent",
                "end": END,
            },
        )
        self.workflow = workflow.compile()

    def agent_done(self, state):
        messages = state["messages"]
        last_message = messages[-1]
        # If there is no function call, then we finish
        if not last_message.tool_calls:
            return "end"
        # Otherwise if there is, we continue
        else:
            return "continue"

    def wait_for_human(self, state):
        messages = state["messages"]
        last_message = messages[-1]
        if (
            isinstance(last_message, ToolMessage)
            and last_message.name is not None
            and last_message.name.startswith("human_")
        ):
            log.info("Waiting for human input")
            return "end"
        else:
            return "continue"

    def _call(self, messages: list[BaseMessage]):
        #messages = messages[:-self.history_window]
        key = "".join([str(m.content) for m in messages])
        if key in self.cache:
            return self.cache[key]
        # ainvoke breaks :(
        #response = await self.llm.ainvoke(messages)
        response = self.llm.invoke(messages)
        self.cache[key] = response
        return response

    def call_model(self, state):
        messages = state["messages"]
        if len(messages) == 1:
            messages.insert(
                0,
                SystemMessage(
                    content=self.system_prompt
                    + f" Today's date is: {datetime.now().strftime('%Y-%m-%d')}."
                ),
            )
        # TODO: filter messages
        #log.info("Calling model with last message %s", messages[-1])
        # response = self.llm.invoke(messages)
        response = self._call(messages)
        return {"messages": [response]}

    def call_tool(self, state):
        messages = state["messages"]
        last_message = messages[-1]
        #log.info("Calling tool with last message: %s", last_message.tool_calls)
        response = self.tool_node.invoke(state)
        # log.info("Tool response: %s %s", type(response), response)
        return response

    def get_graph(self):
        return self.workflow
