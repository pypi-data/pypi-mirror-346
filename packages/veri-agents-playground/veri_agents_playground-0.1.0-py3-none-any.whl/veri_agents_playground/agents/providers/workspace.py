"""Workspace definitions. Workspaces organize workflows and knowledgebases. """

import logging
from typing import Optional

from hydra.utils import instantiate
from omegaconf import DictConfig
from veri_agents_playground.agents.workspace import Workspace

log = logging.getLogger(__name__)


class WorkspaceProvider:
    workspaces: dict[str, "Workspace"] = {}

    @staticmethod
    def get_workspace(name: str) -> Optional["Workspace"]:
        """Get a Workspace by name."""
        return WorkspaceProvider.workspaces.get(name, None)

    @staticmethod
    def get_workspaces() -> dict[str, "Workspace"]:
        """Get all registered workspaces."""
        return WorkspaceProvider.workspaces

    @staticmethod
    def register_workspace(name: str, workspace: "Workspace"):
        """Register a workspace."""
        if name in WorkspaceProvider.workspaces:
            raise ValueError(f"Workspace '{name}' already exists.")
        WorkspaceProvider.workspaces[name] = workspace

    @staticmethod
    def register_from_config(config: DictConfig):
        """Register workspaces from a Hydra/OmegaConf configuration."""
        for wf_name, wf_conf in config.workspaces.items():
            log.info("Registering workspaces %s (%s)", wf_name, wf_conf)
            WorkspaceProvider.register_workspace(wf_name, instantiate(wf_conf, _convert_="all"))
