from omegaconf import DictConfig, OmegaConf

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
        from qdrant_client import QdrantClient, models
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