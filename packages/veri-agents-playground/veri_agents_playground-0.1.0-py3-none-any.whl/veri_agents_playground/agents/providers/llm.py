import logging
from typing import List
from omegaconf import DictConfig
from hydra.utils import instantiate
from langchain_core.language_models import BaseLanguageModel
from langchain_core.embeddings.embeddings import Embeddings

log = logging.getLogger(__name__)


class LLMProvider:
    """Language model abstraction."""

    llms: dict[str, BaseLanguageModel] = {}

    def __init__(self):
        pass

    @staticmethod
    def get_llm(name: str) -> BaseLanguageModel | None:
        """Get an LLM by name."""
        return instantiate(LLMProvider.llms[name], _convert_="all") if name in LLMProvider.llms else None

    @staticmethod
    def get_embeddings(name: str) -> Embeddings | None:
        """Get an embedding model by name."""
        return instantiate(LLMProvider.llms[name], _convert_="all") if name in LLMProvider.llms else None

    @staticmethod
    def get_llm_names() -> List[str]:
        """Get all registered LLMs."""
        return list(LLMProvider.llms.keys())

    @staticmethod
    def register_llm(name: str, llm_conf):
        """Register an LLM, actual LLM class instantiated lazily."""
        if name in LLMProvider.llms:
            raise ValueError(f"LLM '{name}' already exists.")
        LLMProvider.llms[name] = llm_conf

    @staticmethod
    def register_from_config(config: DictConfig):
        """Register LLM models from a Hydra/OmegaConf configuration."""
        for llm_name, llm_conf in config.llms.items():
            log.info("Registering LLM %s (%s)", llm_name, llm_conf)
            LLMProvider.register_llm(llm_name, llm_conf)
