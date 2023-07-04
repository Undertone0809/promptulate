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

from typing import Optional, Union, Dict, Any

from pydantic import Field, validator

from promptulate import utils
from promptulate.config import Config
from promptulate.frameworks.schema import BasePromptFramework
from promptulate.llms import ChatOpenAI
from promptulate.llms.base import BaseLLM
from promptulate.memory import BufferChatMemory
from promptulate.memory.base import BaseChatMemory
from promptulate.preset_roles.roles import CustomPresetRole, get_preset_role_prompt
from promptulate.provider.mixins import (
    SummarizerMixin,
    TranslatorMixin,
    DeriveHistoryMessageMixin,
)
from promptulate.schema import (
    MessageSet,
    AssistantMessage,
    init_chat_message_history,
)
from promptulate.tips import EmptyMessageSetError
from promptulate.utils.core_utils import record_time

CFG = Config()
logger = utils.get_logger()


class Conversation(
    BasePromptFramework, SummarizerMixin, TranslatorMixin, DeriveHistoryMessageMixin
):
    """
    You can use Conversation start a conversation. Moreover, you can pass some parameters to enhance it.

    Attributes
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
    llm: BaseLLM = Field(default_factory=ChatOpenAI)
    enable_stream: bool = False  # streaming transmission
    role: Union[str, CustomPresetRole] = "default-role"
    memory: BaseChatMemory = Field(default_factory=BufferChatMemory)

    @validator("conversation_id", always=True)
    def init_conversation_id(
        cls, conversation_id: Optional[str], values: Dict[str, Any]
    ) -> Optional[str]:
        """initialize self.conversation_id and memory.conversation_id"""
        if not conversation_id:
            return None

        assert conversation_id.isdigit(), "conversation_id must a digit type string"
        if "memory" in values and values["memory"]:
            cls.memory.conversation_id = conversation_id
        return conversation_id

    @validator("memory", always=True)
    def init_memory(
        cls, memory: BaseChatMemory, values: Dict[str, Any]
    ) -> BaseChatMemory:
        """check whether exist conversation_id before initialize memory"""
        if "conversation_id" in values and values["conversation_id"]:
            memory.conversation_id = values["conversation_id"]
        else:
            values["conversation_id"] = memory.conversation_id
            cls.conversation_id = memory.conversation_id
        return memory

    @record_time()
    def predict(self, prompt: str, **kwargs) -> str:
        try:
            messages_history: MessageSet = self.memory.load_message_set_from_memory()
            messages_history.add_user_message(message=prompt)
        except EmptyMessageSetError as e:
            messages_history = init_chat_message_history(
                get_preset_role_prompt(self.role), prompt
            )
            self.memory.save_message_set_to_memory(messages_history)
        logger.debug(
            f"[promptulate Conversation] conversation_id: <{self.conversation_id}> messages: <{messages_history.messages}>"
        )
        prompt_params = {"prompts": messages_history}
        if "stop" in kwargs:
            prompt_params.update({"update": kwargs["stop"]})

        answer: AssistantMessage = self.llm.generate_prompt(**prompt_params)
        messages_history.messages.append(answer)
        self.memory.save_message_set_to_memory(messages_history)
        return answer.content
