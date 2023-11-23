# Copyright (c) 2023 promptulate
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/promptulate
# Contact Email: zeeland@foxmail.com

import logging
from typing import Dict, List, Optional

from cushy_storage.orm import BaseORMModel, CushyOrmCache
from pydantic import BaseModel, Field

from promptulate.utils.core_utils import get_cache
from promptulate.utils.singleton import singleton

logger = logging.getLogger(__name__)

KEY_MODELS_MAPPER = {
    "text-davinci-003": "gpt-3.5-turbo",
    "gpt-3.5-turbo": "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k": "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301": "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613": "gpt-3.5-turbo",
    "gpt-4": "gpt-4",
    "gpt-4-0314": "gpt-4",
    "gpt-4-0613": "gpt-4",
    "gpt-4-32k": "gpt-4",
    "gpt-4-32k-0314": "gpt-4",
    "gpt-4-32k-0613": "gpt-4",
}


class OpenAIKey(BaseORMModel):
    def __init__(self, model: str, key: str):
        super().__init__()
        self.model = model
        self.key = key


def _parse_openai_keys(keys: List[Dict[str, str]]) -> List[OpenAIKey]:
    """parse list of openai keys to OpenAIKey

    Args:
        keys: There are 2 kind of method to input keys
        1.
            keys = [
                {"model": "gpt-3.5-turbo","keys": "key1,key2,key3"},
                {"model": "gpt-4.0","keys": "key4,key5,key6"},
            ]
        2.
            keys = [
            {"model": "gpt-3.5-turbo","key": "key1"},
            {"model": "gpt-3.5-turbo","key": "key2"},
            {"model": "gpt-4.0","key": "key3"},
        ]
    Returns:
        List of OpenAIKey
    """
    openai_keys: List[OpenAIKey] = []
    for key in keys:
        if "key" in key and key["key"]:
            openai_keys.append(OpenAIKey(KEY_MODELS_MAPPER[key["model"]], key["key"]))
        elif "keys" in key and key["keys"]:
            _keys = key["keys"].split(",")
            for _key in _keys:
                openai_keys.append(OpenAIKey(KEY_MODELS_MAPPER[key["model"]], _key))
        else:
            raise ValueError("Key type error, your field name must be `key` or `keys`")
    return openai_keys


@singleton()
class OpenAIKeyPool(BaseModel):
    """todo provide key expiration check and token balance check"""

    cache: CushyOrmCache = Field(default_factory=get_cache)

    class Config:
        arbitrary_types_allowed = True

    def get(self, model: str) -> Optional[str]:
        """Obtain the openai key from the queue header and return it, then place the key
        at the end of queue. Use gpt4 key if the gpt3.5 key does not exist.

        Args:
            model: openai model, the option is as follows:
                "text-davinci-003","gpt-3.5-turbo","gpt-3.5-turbo-16k","gpt-3.5-turbo-0301","gpt-3.5-turbo-0613",
                "gpt-4","gpt-4-0314","gpt-4-0613","gpt-4-32k","gpt-4-32k-0314","gpt-4-32k-0613"

        Returns:
            specified openai key
        """
        model = KEY_MODELS_MAPPER[model]
        openai_key: OpenAIKey = self.cache.query(OpenAIKey).filter(model=model).first()

        if not openai_key:
            if model == "gpt-4":
                return None

            model = "gpt-4"
            openai_key: OpenAIKey = (
                self.cache.query(OpenAIKey).filter(model=model).first()
            )
            if not openai_key:
                return None

        self.cache.delete(openai_key)
        self.cache.add(openai_key)
        return openai_key.key

    def set(self, keys: List[Dict[str, str]]):
        """Set list of key to cache, you can see parameter description from
        `_parse_openai_keys()`"""
        self.cache.set(_parse_openai_keys(keys))
        logger.info("[promptulate] OpenAIKeyPool set key successfully.")

    def add(self, keys: List[Dict[str, str]]):
        """add list of keys to cache, you can see parameter description from
        `_parse_openai_keys()`"""
        self.cache.add(_parse_openai_keys(keys))

    def delete(self, key: str, model: Optional[str] = None):
        if model:
            openai_key: OpenAIKey = (
                self.cache.query(OpenAIKey).filter(key=key, model=model).first()
            )
        else:
            openai_key: List[OpenAIKey] = (
                self.cache.query(OpenAIKey).filter(key=key).all()
            )
        self.cache.delete(openai_key)

    def get_num(self, model: str) -> int:
        return len(self.cache.query(OpenAIKey).filter(model=model).all())

    def all(self) -> List[Dict]:
        results = []
        openai_keys = self.cache.query(OpenAIKey).all()
        for openai_key in openai_keys:
            results.append(openai_key.__dict__)
        return results


def export_openai_key_pool(keys: List[Dict[str, str]]):
    OpenAIKeyPool().set(keys)


def add_key_to_key_pool(keys: List[Dict[str, str]]):
    openai_key_pool = OpenAIKeyPool()
    openai_key_pool.add(keys)
