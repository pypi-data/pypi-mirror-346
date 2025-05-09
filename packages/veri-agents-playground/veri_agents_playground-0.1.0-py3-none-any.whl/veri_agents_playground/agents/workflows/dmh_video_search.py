"""Example workflow"""

import logging
import operator
from typing import Annotated, List, Sequence, TypedDict, cast

from langchain_core.messages import AnyMessage
from langchain_core.messages import HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from veri_agents_playground.agents.providers import LLMProvider, ToolProvider
from veri_agents_playground.agents.workflow import Workflow

log = logging.getLogger(__name__)


class AgentState(TypedDict):
    messages: Annotated[Sequence[AnyMessage], add_messages]
    retrieved_videos: Annotated[List[dict], operator.add]


class DMHVideoSearch(Workflow):
    def __init__(self, name: str, description: str, icon: str, llm: str, **kwargs):
        super().__init__(name=name, description=description, icon=icon, **kwargs)
        self.llm = cast(BaseChatModel, LLMProvider.get_llm(llm))
        if not self.llm:
            raise ValueError("LLM not found: " + llm)
        dmh_search_tool = ToolProvider.get_tool("dmh_video_search")
        if not dmh_search_tool:
            raise ValueError("Tool not found: dmh_video_search")
        dmh_show_results_tool = ToolProvider.get_tool("dmh_show_results")
        if not dmh_show_results_tool:
            raise ValueError("Tool not found: dmh_show_results")

        self.tools = [dmh_search_tool, dmh_show_results_tool]
        self.tool_node = ToolNode(self.tools)
        self.llm = self.llm.bind_tools(self.tools)

        workflow = StateGraph(AgentState)

        # Define the two nodes we will cycle between
        workflow.add_node("agent", self.call_model)
        workflow.add_node("action", self.call_tool)

        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        workflow.add_edge(START, "agent")

        # We now add a conditional edge
        workflow.add_conditional_edges(
            # First, we define the start node. We use `agent`.
            # This means these are the edges taken after the `agent` node is called.
            "agent",
            # Next, we pass in the function that will determine which node is called next.
            self.should_continue,
            # Finally we pass in a mapping.
            # The keys are strings, and the values are other nodes.
            # END is a special node marking that the graph should finish.
            # What will happen is we will call `should_continue`, and then the output of that
            # will be matched against the keys in this mapping.
            # Based on which one it matches, that node will then be called.
            {
                # If `tools`, then we call the tool node.
                "continue": "action",
                # Otherwise we finish.
                "end": END,
            },
        )

        # We now add a normal edge from `tools` to `agent`.
        # This means that after `tools` is called, `agent` node is called next.
        workflow.add_edge("action", "agent")

        # Finally, we compile it!
        # This compiles it into a LangChain Runnable,
        # meaning you can use it as you would any other runnable
        #saver = WorkflowPersistence.get_saver()
        self.workflow = workflow.compile()

    # Define the function that determines whether to continue or not
    def should_continue(self, state):
        messages = state["messages"]
        last_message = messages[-1]
        # If there is no function call, then we finish
        if not last_message.tool_calls:
            return "end"
        # Otherwise if there is, we continue
        else:
            return "continue"

    # Define the function that calls the model
    def call_model(self, state):
        messages = state["messages"]
        log.info("Calling model with messages %s", messages)
        response = self.llm.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}

    # Define the function to execute tools
    def call_tool(self, state):
        messages = state["messages"]
        last_message = messages[-1]
        log.info(f"Last message: {last_message}")
        tool_call = last_message.tool_calls[0]
        log.info("Calling tool %s with call id %s and args %s", tool_call["name"], tool_call['id'], tool_call["args"])
        response = self.tool_node.invoke(state)
        log.info("Tool response: %s %s", type(response), response)
        return response

    def invoke(self, message: str):
        inputs = {"messages": [HumanMessage(content=message)]}
        #return self.workflow.invoke(inputs)
        for output in self.workflow.stream(inputs):
            # stream() yields dictionaries with output keyed by node name
            for key, value in output.items():
                print(f"Output from node '{key}':")
                print("---")
                print(type(value))
                print(value)
            print("\n---\n")

    def get_graph(self):
        return self.workflow
