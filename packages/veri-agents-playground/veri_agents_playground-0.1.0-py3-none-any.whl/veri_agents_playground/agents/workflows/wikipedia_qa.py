import logging

from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langgraph.prebuilt import create_react_agent

from veri_agents_playground.agents.providers import LLMProvider
from veri_agents_playground.agents.workflow import Workflow

log = logging.getLogger(__name__)


class WikipediaQA(Workflow):
    def __init__(self, name: str, description: str, llm: str, icon: str, **kwargs):
        super().__init__(name=name, description=description, icon=icon, **kwargs)
        self.llm = LLMProvider.get_llm(llm)
        if not self.llm:
            raise ValueError("LLM not found: " + llm)
        self.tools = [WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())] # pyright: ignore[reportCallIssue]

        self.workflow = create_react_agent(
            model=self.llm,
            tools=self.tools
        )

    def get_graph(self):
        return self.workflow
