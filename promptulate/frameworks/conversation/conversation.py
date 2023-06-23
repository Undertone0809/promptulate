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

from pydantic import Field
from typing import Optional, Union

from promptulate import utils
from promptulate.config import Config
from promptulate.llms import OpenAI
from promptulate.llms.base import BaseLLM
from promptulate.memory import BufferChatMemory
from promptulate.memory.base import BaseChatMemory
from promptulate.utils.core_utils import record_time
from promptulate.tips import EmptyChatMessageHistoryTip
from promptulate.preset_roles.roles import CustomPresetRole, get_preset_role_prompt
from promptulate.provider.mixins import (
    SummarizerMixin,
    TranslatorMixin,
    DeriveHistoryMessageMixin,
)
from promptulate.frameworks.schema import BasePromptFramework
from promptulate.schema import (
    LLMPrompt,
    AssistantMessage,
    ChatMessageHistory,
    init_chat_message_history,
)

CFG = Config()
logger = utils.get_logger()


class Conversation(
    BasePromptFramework, SummarizerMixin, TranslatorMixin, DeriveHistoryMessageMixin
):
    """
    You can use Conversation start a conversation. Moreover, you can pass some parameters to enhance it.

    Args
        role: preset role. Default is default role.
        llm: default is OpenAI GPT3.5. You can choose other llm.
        conversation_id: conversation id. Default is None
        memory: the way you want to store chat data. Default is BufferChatMemory, which is used
            for local file storage.

    Examples
        from promptulate import Conversation

        conversation = Conversation()
        conversation.predict("Hello, Who are you?")
    """

    conversation_id: Optional[str] = None
    llm: BaseLLM = Field(default_factory=OpenAI)
    enable_stream: bool = False  # streaming transmission
    role: Union[str, CustomPresetRole] = "default-role"
    memory: BaseChatMemory = Field(default_factory=BufferChatMemory)

    @record_time()
    def predict(self, prompt: str) -> str:
        try:
            messages_history: ChatMessageHistory = (
                self.memory.load_conversation_from_memory(self.conversation_id)
            )
            messages_history.add_user_message(message=prompt)
        except EmptyChatMessageHistoryTip as e:
            messages_history = init_chat_message_history(
                get_preset_role_prompt(self.role), prompt
            )
            self.conversation_id = messages_history.conversation_id
            self.memory.save_conversation_to_memory(messages_history)
        logger.debug(f"[promptulate Conversation] {messages_history.messages}")
        logger.info(
            f"[promptulate Conversation] ask: {messages_history.messages[-1].content}"
        )
        answer: AssistantMessage = self.llm.generate_prompt(
            LLMPrompt(messages=messages_history.messages)
        )
        logger.info(f"[promptulate Conversation] answer: {answer}")
        messages_history.messages.append(answer)
        self.memory.save_conversation_to_memory(messages_history)
        return answer.content
