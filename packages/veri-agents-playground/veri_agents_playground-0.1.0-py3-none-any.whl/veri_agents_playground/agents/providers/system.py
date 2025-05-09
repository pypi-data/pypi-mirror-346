from omegaconf import DictConfig

from .workflow import WorkflowProvider
from .llm import LLMProvider
from .tool import ToolProvider
from .persistence import AssetsManager
from .knowledgebase import KnowledgebaseProvider
from .workspace import Workspace
from .knowledgebase import KnowledgebaseProvider
from .workspace import WorkspaceProvider
from veri_agents_playground.agents.access import AccessControl


def init_from_config(cfg: DictConfig, access_control: AccessControl | None = None):
    """ Register tools, LLMs, workflows. """
    WorkspaceProvider.register_from_config(cfg)
    ToolProvider.register_from_config(cfg)
    LLMProvider.register_from_config(cfg)
    KnowledgebaseProvider.register_from_config(cfg)
    WorkflowProvider.register_from_config(cfg, access_control=access_control)
    AssetsManager.register_from_config(cfg)


async def ainit_from_config(cfg: DictConfig, access_control: AccessControl | None = None):
    """ Register tools, LLMs, workflows. """
    WorkspaceProvider.register_from_config(cfg)
    #ToolProvider.register_from_config(cfg)
    await ToolProvider.aregister_from_config(cfg)
    LLMProvider.register_from_config(cfg)
    KnowledgebaseProvider.register_from_config(cfg)
    WorkflowProvider.register_from_config(cfg, access_control=access_control)
    AssetsManager.register_from_config(cfg)
