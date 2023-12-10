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

import warnings
from typing import Any, Dict, Optional, Union

from pydantic import Field, validator

from promptulate.error import EmptyMessageSetError
from promptulate.frameworks.schema import BasePromptFramework
from promptulate.llms import ChatOpenAI
from promptulate.llms.base import BaseLLM
from promptulate.memory import BufferChatMemory
from promptulate.memory.base import BaseChatMemory
from promptulate.preset_roles.roles import CustomPresetRole, get_preset_role_prompt
from promptulate.provider.mixins import (
    DeriveHistoryMessageMixin,
    SummarizerMixin,
    TranslatorMixin,
)
from promptulate.schema import (
    BaseMessage,
    LLMType,
    MessageSet,
    UserMessage,
    init_chat_message_history,
)
from promptulate.utils.logger import logger


class Conversation(
    BasePromptFramework, SummarizerMixin, TranslatorMixin, DeriveHistoryMessageMixin
):
    """
    You can use Conversation start a conversation. Moreover, you can pass some
    parameters to enhance it.

    Attributes
        role: preset role. Default is default role.
        llm: default is ChatOpenAI GPT3.5. You can choose other llm.
        conversation_id: conversation id. Default is None
        memory: the way you want to store chat data. Default is BufferChatMemory, which
            is used for local file storage.

    Examples
        from promptulate import Conversation

        conversation = Conversation()
        conversation.run("Hello, Who are you?")
    """

    conversation_id: Optional[str] = None
    llm: BaseLLM = Field(default_factory=ChatOpenAI)
    enable_stream: bool = False  # streaming transmission
    role: Union[str, CustomPresetRole] = "default-role"
    memory: BaseChatMemory = Field(default_factory=BufferChatMemory)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.role == "default-role" and self.llm.llm_type == LLMType.ErnieBot:
            self.role = "ernie-default-role"

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

    def predict(self, prompt: str, **kwargs) -> str:
        return self.run(prompt, **kwargs)

    def run_by_message_set(self, message_set: MessageSet, *args, **kwargs) -> str:
        answer: BaseMessage = self.llm.predict(message_set, *args, **kwargs)
        message_set.add_message(answer)
        self.memory.save_message_set_to_memory(message_set)
        return answer.content

    def run(
        self, prompt: str, custom_system_prompt: bool = False, *args, **kwargs
    ) -> str:
        warnings.warn(
            "Conversation will be deprecated at v1.7.0, please use promptulate.agents.LLMAgent",  # noqa
            DeprecationWarning,
        )
        try:
            messages_history: MessageSet = self.memory.load_message_set_from_memory()
            messages_history.add_user_message(message=prompt)
        except EmptyMessageSetError:
            if custom_system_prompt:
                messages_history = MessageSet(messages=[UserMessage(content=prompt)])
            else:
                messages_history = init_chat_message_history(
                    get_preset_role_prompt(self.role), prompt, self.llm.llm_type
                )
                self.memory.save_message_set_to_memory(messages_history)
        logger.debug(
            f"[pne Conversation] conversation_id: <{self.conversation_id}> messages: <{messages_history.messages}>"  # noqa
        )
        prompt_params = {"prompts": messages_history}
        if "stop" in kwargs:
            prompt_params.update({"stop": kwargs["stop"]})

        answer: BaseMessage = self.llm.predict(**prompt_params)
        messages_history.messages.append(answer)
        self.memory.save_message_set_to_memory(messages_history)
        return answer.content
