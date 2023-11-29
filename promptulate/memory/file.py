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

from typing import Optional

from cushy_storage import CushyOrmCache
from pydantic import Field, validator

from promptulate.error import EmptyMessageSetError
from promptulate.memory.base import BaseChatMemory
from promptulate.schema import MessageSet


class FileChatMemory(BaseChatMemory):
    """Chat message will be stored in the local file cache."""

    file_path: Optional[str] = None
    """If you want to change default store path, you can set specified file_path"""
    cache: CushyOrmCache = Field(default_factory=CushyOrmCache)

    @validator("file_path", always=True)
    def init_cache(cls, file_path: Optional[str]) -> Optional[str]:
        if not file_path:
            return None

        cls.cache = CushyOrmCache(file_path)
        return file_path

    def load_message_set_from_memory(
        self, recently_n: Optional[int] = None
    ) -> MessageSet:
        """Load message from file memory

        Args:
            recently_n: load all messages if it is None, or return recently n messages.

        Returns:
            messages wrapping by MessageSet
        """
        if self.conversation_id not in self.cache:
            raise EmptyMessageSetError()
        return MessageSet.from_listdict_data(self.cache[self.conversation_id])

    def save_message_set_to_memory(self, message_set: MessageSet) -> None:
        self.cache[self.conversation_id] = message_set.listdict_messages
