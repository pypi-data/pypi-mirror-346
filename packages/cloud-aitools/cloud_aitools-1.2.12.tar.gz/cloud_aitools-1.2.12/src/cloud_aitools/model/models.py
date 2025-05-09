import logging
from dataclasses import dataclass
import json
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


@dataclass
class UploadObject:
    filepath: str
    bucket: str
    object_key: str
    relative_path: str


class ObjectIndex(BaseModel):
    filename: str
    bucket: str
    object_key: str
    url: str


class ModelIndex(BaseModel):
    model_name: str
    file_list: list[ObjectIndex]


class Index:

    def __init__(self, index_config: list[dict[str, Any]]) -> None:
        self.index_config = index_config
        self.model_config: dict[str, ModelIndex] = self.load_config(
            self.index_config)

    def load_config(self, index_config: list[dict[str, Any]]):
        res = {}
        logger.debug("Loading index configuration with %d models",
                     len(index_config))
        for model_item in index_config:
            item = ModelIndex.model_validate(model_item)
            res[item.model_name] = item
            logger.debug("Loaded model: %s with %d files", item.model_name,
                         len(item.file_list))
        logger.info("Loaded configuration for %d models", len(res))
        return res

    def update(self, model_index_config: ModelIndex):
        logger.info("Updating index for model: %s",
                    model_index_config.model_name)
        logger.debug("Model has %d files", len(model_index_config.file_list))
        self.model_config[model_index_config.model_name] = model_index_config

    def dump(self):
        logger.debug("Dumping index configuration")
        dumped = [model.model_dump() for model in self.model_config.values()]
        logger.info("Dumped configuration for %d models", len(dumped))
        return json.dumps(dumped)

    def get_model_objects_index(self, model_name: str):
        return self.model_config[model_name].file_list

    def get_all_model_index(self):
        return self.model_config.values()