from typing import Optional

from hydra.utils import instantiate
from omegaconf import DictConfig

from veri_agents_playground.agents.persistence import AssetsStorage

class AssetsManager:
    assets_storage: Optional[AssetsStorage] = None

    @staticmethod
    def register_from_config(config: DictConfig):
        # FIXME
        AssetsManager.assets_storage = instantiate(config.assets_storage, _convert_="all")

    @staticmethod
    def get_storage() -> AssetsStorage:
        if AssetsManager.assets_storage is None:
            raise ValueError("Assets storage not initialized.")
        return AssetsManager.assets_storage

# @classmethod
# def from_config(cls, config: DictConfig) -> "AssetsFileStorage":
#     return cls(config.assets_manager.location)
