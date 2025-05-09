""" Question answering workflow. """

import logging

from veri_agents_playground.agents.providers import KnowledgebaseProvider, LLMProvider
from veri_agents_playground.agents.workflow import Workflow

from veri_agents_knowledgebase.graphs import create_qa_agent

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
        kb = KnowledgebaseProvider.get_knowledgebase(knowledgebase)
        if kb is None:
            raise ValueError("Knowledgebase not found: " + knowledgebase)

        self.workflow = create_qa_agent(
            llm=self.llm,
            knowledgebases=[kb],
            system_prompt=system_prompt,
            debug=True
        )

    def get_graph(self):
        return self.workflow
