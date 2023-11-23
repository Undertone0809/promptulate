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
from abc import abstractmethod
from typing import Any, Dict, Optional

from pydantic import BaseModel

from promptulate.schema import MessageSet
from promptulate.utils.core_utils import generate_conversation_id


class BaseMemory(BaseModel):
    store: Any
    """storage medium"""

    def query(self, key: str) -> Any:
        ...

    def update(self, key: str, value: str) -> Any:
        ...

    def clear(self, key: str) -> Any:
        ...

    def append(self, key: str, value: str) -> Any:
        ...


class BaseChatMemory(BaseModel):
    """
    Base class for store chat message. By implementing this class, you can implement
    message storage on different storage media. Actually, every Chat Memory is a
    singleton class. It's means there are utils class to read and write chat data.
    """

    summary: str = ""
    conversation_id: Optional[str] = None
    additional_kwargs: Dict[str, Any] = {}

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "conversation_id" not in kwargs:
            self.conversation_id = generate_conversation_id()

    @abstractmethod
    def load_message_set_from_memory(
        self, recently_n: Optional[int] = None
    ) -> MessageSet:
        """Return key-value pairs given the text input to the chain.
        If None, return all memories
        """

    @abstractmethod
    def save_message_set_to_memory(self, inputs: MessageSet) -> None:
        """Save the context of this model run to memory."""
