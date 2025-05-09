import logging
from typing import Any, Optional

from hydra.utils import instantiate
from langchain_core.tools import BaseTool
from omegaconf import DictConfig

log = logging.getLogger(__name__)


class ToolProvider:
    tools: dict[str, BaseTool] = {}

    def __init__(self):
        pass

    @staticmethod
    def get_tool(name: str, **kwargs: Any) -> Optional[BaseTool]:
        """Get a tool by name."""
        log.info(f"Instantiating Tool {name} with kwargs {kwargs}")
        if name not in ToolProvider.tools:
            raise ValueError(f"Tool '{name}' not found.")
        retrieved_tool = ToolProvider.tools[name]
        if isinstance(retrieved_tool, BaseTool):
            return retrieved_tool
        return instantiate(retrieved_tool, _convert_="all", **kwargs) if name in ToolProvider.tools else None

    @staticmethod
    def register_tool(name: str, tool_conf):
        """Register a tool, instantiated lazily. """
        if name in ToolProvider.tools:
            raise ValueError(f"Tool '{name}' already exists.")
        ToolProvider.tools[name] = tool_conf

    @staticmethod
    def register_from_config(config: DictConfig):
        """Register tools from a Hydra/OmegaConf configuration."""
        for tool_name, tool_conf in config.tools.items():
            log.info("Registering Tool %s (%s)", tool_name, tool_conf)
            ToolProvider.register_tool(tool_name, tool_conf)

    @staticmethod
    async def aregister_from_config(config: DictConfig):
        """Register tools from a Hydra/OmegaConf configuration."""
        for tool_name, tool_conf in config.tools.items():
            log.info("Registering Tool %s (%s)", tool_name, tool_conf)
            ToolProvider.register_tool(tool_name, tool_conf)
            # TODO: register MCP tools
        
