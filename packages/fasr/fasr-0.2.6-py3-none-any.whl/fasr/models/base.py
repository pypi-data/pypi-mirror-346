from fasr.config import Config
from fasr.utils.base import CheckpointMixin, IOMixin
from pathlib import Path
from typing_extensions import Self
from typing import Dict
from pydantic import ConfigDict
from abc import abstractmethod


class Model(CheckpointMixin, IOMixin):
    model_config: ConfigDict = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True
    )

    def get_config(self) -> Config:
        raise NotImplementedError

    def load(self, save_dir: str | Path, **kwargs) -> Self:
        raise NotImplementedError

    def save(self, save_dir: str | Path, **kwargs) -> None:
        raise NotImplementedError

    def from_checkpoint(self, checkpoint_dir: str | Path, **kwargs) -> Self:
        raise NotImplementedError


class CachedModel(Model):
    model_config: ConfigDict = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True
    )

    cache: Dict = {}

    @abstractmethod
    def reset(self):
        raise NotImplementedError
