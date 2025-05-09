"""Example workflow"""

import logging

from veri_agents_knowledgebase.graphs import create_qa_agent

from veri_agents_playground.agents.providers import LLMProvider, KnowledgebaseProvider
from veri_agents_playground.agents.workflow import Workflow

log = logging.getLogger(__name__)

class QuestionAnswering(Workflow):
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
        super().__init__(name=name, description=description, icon=icon, **kwargs)
        self.llm = LLMProvider.get_llm(llm)
        if not self.llm:
            raise ValueError("LLM not found: " + llm)

        self.knowledgebase = KnowledgebaseProvider.get_knowledgebase(knowledgebase)
        if not self.knowledgebase:
            raise ValueError("Knowledgebase not found: " + llm)

        self.system_prompt = system_prompt

        self.workflow = create_qa_agent(
            llm=self.llm,
            knowledgebases=[self.knowledgebase],
            system_prompt=self.system_prompt,
        )

    def get_graph(self):
        return self.workflow
