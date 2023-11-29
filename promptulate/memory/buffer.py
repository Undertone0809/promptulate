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

from typing import Dict, List, Optional

from promptulate.error import EmptyMessageSetError
from promptulate.memory.base import BaseChatMemory
from promptulate.schema import MessageSet

buffer: Dict[str, List[Dict]] = {}
"""global message buffer, here is a buffer example:
{
    "conversation_id1": [message...],
    "conversation_id2": [message...],
}
"""


class BufferChatMemory(BaseChatMemory):
    """Chat message will be stored in the buffer cache."""

    def load_message_set_from_memory(
        self, recently_n: Optional[int] = None
    ) -> MessageSet:
        """Load message from buffer memory

        Args:
            recently_n: load all messages if it is None, or return recently n messages.

        Returns:
            messages wrapping by MessageSet
        """
        if not buffer:
            raise EmptyMessageSetError
        recently_n = recently_n if recently_n else len(buffer[self.conversation_id])
        num_messages = len(buffer[self.conversation_id])
        return MessageSet.from_listdict_data(
            buffer[self.conversation_id][num_messages - recently_n :]
        )

    def save_message_set_to_memory(self, message_set: MessageSet) -> None:
        buffer[self.conversation_id] = message_set.memory_messages
