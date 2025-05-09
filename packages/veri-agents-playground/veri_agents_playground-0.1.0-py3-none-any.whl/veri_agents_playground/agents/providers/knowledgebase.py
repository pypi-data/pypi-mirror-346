import logging
from typing import Optional, cast

from hydra.utils import instantiate
from omegaconf import DictConfig
from veri_agents_knowledgebase import Knowledgebase, KnowledgebaseMetadata

log = logging.getLogger(__name__)

class KnowledgebasesStore:
    """A store for keeping additional (i.e. in addition to the ones defined in the config) knowledge bases."""

    def __init__(self):
        pass

    def add_knowledgebase(self, kb):
        """Add a knowledge base to the store."""
        raise NotImplementedError

    def get_knowledgebases(self) -> dict[str, DictConfig]:
        """Get all knowledge bases."""
        raise NotImplementedError


class QdrantKnowledgebasesStore(KnowledgebasesStore):
    """A store for Qdrant knowledge bases."""

    def __init__(self, db_url: str):
        super().__init__()
        from qdrant_client import QdrantClient
        self.collection_name = "knowledgebases"
        self.client = QdrantClient(db_url)
        self.create_schema(delete_existing=False)

    def create_schema(self, delete_existing: bool = False) -> None:
        if delete_existing and self.client.collection_exists(self.collection_name):
            self.client.delete_collection(self.collection_name)
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(self.collection_name, vectors_config={})

    def get_knowledgebases(self) -> dict[str, DictConfig]:
        offset = 0
        ret = {}
        while offset is not None:
            points, offset = self.client.scroll(self.collection_name, with_payload=True, with_vectors=False, offset=offset)
            for point in points:
                if point is not None and point.payload is not None:
                    ret[point.payload["name"]] = DictConfig(point.payload["config"])
        return ret

class KnowledgebaseProvider:
    knowledge_bases: dict[str, DictConfig] = {}
    knowledge_base_store: Optional[KnowledgebasesStore] = None

    @staticmethod
    def get_knowledgebases() -> dict[str, "Knowledgebase"]:
        """Get all registered knowledgebases."""
        return {
            name: instantiate(kb_conf, _convert_='all')
            for name, kb_conf in KnowledgebaseProvider.knowledge_bases.items()
        }

    @staticmethod
    def get_knowledgebases_metadata() -> dict[str, KnowledgebaseMetadata]:
        """Get metadata for all registered knowledgebases."""
        return {
            name: kb.metadata for name, kb in KnowledgebaseProvider.get_knowledgebases().items()
        }

    @staticmethod
    def get_knowledgebase(name: str) -> Optional[Knowledgebase]:
        """Get a knowledge base by name."""
        return (
            instantiate(KnowledgebaseProvider.knowledge_bases[name], _convert_="all")
            if name in KnowledgebaseProvider.knowledge_bases
            else None
        )

    @staticmethod
    def register_knowledgebase(name: str, kb_conf):
        """Register a knowledge base, instantiated lazily."""
        if name in KnowledgebaseProvider.knowledge_bases:
            raise ValueError(f"Knowledge base '{name}' already exists.")
        KnowledgebaseProvider.knowledge_bases[name] = kb_conf

    @staticmethod
    def register_from_config(config: DictConfig):
        """Register all knowledge bases from a Hydra/OmegaConf configuration."""
        for kb_name, kb_conf in config.knowledgebases.items():
            log.info("Registering Knowledge Base %s (%s)", kb_name, kb_conf)
            KnowledgebaseProvider.register_knowledgebase(kb_name, kb_conf)

        # get additional knowledge bases from the database
        #for kb_name, kb_conf in KnowledgebaseLoader._get_knowledgebases_from_store(
        #    config
        #).items():
        #    log.info("Registering Knowledge Base from store: %s (%s)", kb_name, kb_conf)
        #    KnowledgebaseLoader.register_knowledgebase(kb_name, kb_conf)

    @staticmethod
    def _get_knowledgebases_from_store(config: DictConfig) -> dict[str, DictConfig]:
        """Get knowledge bases from the store."""
        if KnowledgebaseProvider.knowledge_base_store is None:
            KnowledgebaseProvider.knowledge_base_store = instantiate(config.knowledgebase_store, _convert_="all")

        return cast(KnowledgebasesStore, KnowledgebaseProvider.knowledge_base_store).get_knowledgebases()
