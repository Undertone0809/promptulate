# Copyright (c) 2023 Zeeland
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

from typing import List, Dict, Optional

from cushy_storage.orm import CushyOrmCache, BaseORMModel
from pydantic import BaseModel, Field

from promptulate.utils.core_utils import get_cache
from promptulate.utils.singleton import singleton


class OpenAIKey(BaseORMModel):
    def __init__(self, model: str, key: str):
        super().__init__()
        self.model = model
        self.key = key


@singleton()
class OpenAIKeyPool(BaseModel):
    """todo provide key expiration check"""

    cache: CushyOrmCache = Field(default_factory=get_cache)

    class Config:
        arbitrary_types_allowed = True

    def get(self, model: str) -> Optional[str]:
        openai_key: OpenAIKey = self.cache.query(OpenAIKey).filter(model=model).first()
        if not openai_key:
            return None

        self.cache.delete(openai_key)
        self.cache.add(openai_key)
        return openai_key.key

    def set(self, keys: List[Dict[str, str]]):
        openai_keys = list(map(lambda key: OpenAIKey(key["model"], key["key"]), keys))
        self.cache.set(openai_keys)

    def add(self, key: str, model: str):
        if not self.cache.query(OpenAIKey).filter(key=key, model=model).first():
            self.cache.add(OpenAIKey(model, key))

    def delete(self, key: str, model: Optional[str] = None):
        if model:
            openai_key: OpenAIKey = (
                self.cache.query(OpenAIKey).filter(key=key, model=model).first()
            )
        else:
            openai_key: OpenAIKey = self.cache.query(OpenAIKey).filter(key=key).all()
        self.cache.delete(openai_key)

    def get_num(self, model: str) -> int:
        return len(self.cache.query(OpenAIKey).filter(model=model).all())


def export_openai_key_pool(keys: List[Dict[str, str]]):
    OpenAIKeyPool().set(keys)


def add_key_to_key_pool(keys: List[Dict[str, str]]):
    openai_key_pool = OpenAIKeyPool()
    for key_info in keys:
        openai_key_pool.add(**key_info)
