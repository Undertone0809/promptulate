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

from promptulate import utils
from promptulate.tips import EmptyChatMessageHistoryTip
from promptulate.memory.base import BaseChatMemory
from promptulate.schema import (
    ListDictPrompt,
    ChatMessageHistory,
    generate_conversation_id,
)

cache = utils.get_cache()
logger = utils.get_logger()


class LocalCacheChatMemory(BaseChatMemory):
    """Chat message will be stored in the local file cache."""

    def load_conversation_from_memory(self, conversation_id: Optional[str]) -> ChatMessageHistory:
        if conversation_id is None or conversation_id not in cache:
            raise EmptyChatMessageHistoryTip()
        cache_messages = cache[conversation_id]
        return ListDictPrompt(messages=cache_messages).chat_message_history

    def save_conversation_to_memory(self, chat_message_history: ChatMessageHistory) -> None:
        if not chat_message_history.conversation_id:
            chat_message_history.conversation_id = generate_conversation_id()
        cache[chat_message_history.conversation_id] = chat_message_history.listdict_message
