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

from typing import Optional
from abc import abstractmethod

from promptulate import utils
from promptulate.utils import AbstractSingleton
from promptulate.schema import ChatMessageHistory

__all__ = ['BaseChatMemory']


class BaseChatMemory(AbstractSingleton):
    """
    Base class for store chat message. By implementing this class, you can implement
    message storage on different storage media. Actually, every Chat Memory is a singleton
    class. It's means there are utils class to read and write chat data.
    """

    @abstractmethod
    def load_conversation_from_memory(self, conversation_id: Optional[str]) -> ChatMessageHistory:
        """Return key-value pairs given the text input to the chain.
        If None, return all memories
        """

    @abstractmethod
    def save_conversation_to_memory(self, inputs: ChatMessageHistory) -> None:
        """Save the context of this model run to memory."""
