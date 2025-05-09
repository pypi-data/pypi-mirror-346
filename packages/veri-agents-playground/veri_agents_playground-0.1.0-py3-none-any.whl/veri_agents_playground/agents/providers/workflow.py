import logging
from typing import Optional

from hydra.utils import instantiate
from omegaconf import DictConfig
from veri_agents_playground.agents.workflow import Workflow
from veri_agents_playground.agents.access import AccessControl

log = logging.getLogger(__name__)

class WorkflowProvider:
    workflows: dict[str, "Workflow"] = {}

    @staticmethod
    def get_workflow(name: str) -> Optional["Workflow"]:
        """Get a workflow by name."""
        # TODO: potentially instantiate here and provide additional parameters like user ID, thread ID
        return WorkflowProvider.workflows.get(name, None)

    @staticmethod
    def get_workflows() -> dict[str, "Workflow"]:
        """Get all registered workflows."""
        return WorkflowProvider.workflows

    @staticmethod
    def register_workflow(name: str, workflow: "Workflow"):
        """Register a workflow."""
        if name in WorkflowProvider.workflows:
            raise ValueError(f"Workflow '{name}' already exists.")
        WorkflowProvider.workflows[name] = workflow

    @staticmethod
    def register_from_config(
        config: DictConfig, access_control: AccessControl | None = None
    ):
        """Register workflows from a Hydra/OmegaConf configuration."""
        for wf_name, wf_conf in config.workflows.items():
            log.info("Registering workflow %s (%s)", wf_name, wf_conf)
            WorkflowProvider.register_workflow(
                wf_name,
                instantiate(wf_conf, _convert_="all", access_control=access_control),
            )

