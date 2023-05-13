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

import time
from abc import abstractmethod
from typing import List
from pydantic import BaseModel, Field

__all__ = [
    'BaseMessage',
    'BaseChatMessageHistory',
    'SystemMessage',
    'UserMessage',
    'AssistantMessage',
    'ChatMessageHistory',
    'LLMPrompt',
    'ListDictPrompt',
    'generate_conversation_id',
    'init_chat_message_history'
]


class BaseMessage(BaseModel):
    """Message basic object."""

    content: str
    additional_kwargs: dict = Field(default_factory=dict)

    @property
    @abstractmethod
    def type(self) -> str:
        """Type of the message, used for serialization."""


class SystemMessage(BaseMessage):
    """Type of message that is a system message."""

    @property
    def type(self) -> str:
        """Type of the message, used for serialization."""
        return "system"


class UserMessage(BaseMessage):
    """Type of message that is a user message."""

    @property
    def type(self) -> str:
        return "user"


class AssistantMessage(BaseMessage):
    """Type of message that is an assistant message."""

    @property
    def type(self) -> str:
        return "assistant"


class BaseChatMessageHistory(BaseModel):
    """Base interface for chat message history
    See `ChatMessageHistory` for default implementation.
    """

    """
    Example:
        .. code-block:: python

            class FileChatMessageHistory(BaseChatMessageHistory):
                storage_path:  str
                session_id: str

               @property
               def messages(self):
                   with open(os.path.join(storage_path, session_id), 'r:utf-8') as f:
                       messages = json.loads(f.read())
                    return messages_from_dict(messages)

               def add_user_message(self, message: str):
                   message_ = HumanMessage(content=message)
                   messages = self.messages.append(_message_to_dict(_message))
                   with open(os.path.join(storage_path, session_id), 'w') as f:
                       json.dump(f, messages)

               def add_ai_message(self, message: str):
                   message_ = AIMessage(content=message)
                   messages = self.messages.append(_message_to_dict(_message))
                   with open(os.path.join(storage_path, session_id), 'w') as f:
                       json.dump(f, messages)

               def clear(self):
                   with open(os.path.join(storage_path, session_id), 'w') as f:
                       f.write("[]")
    """

    messages: List[BaseMessage]
    conversation_id: str

    @abstractmethod
    def add_system_message(self, message):
        """add a system message"""

    @abstractmethod
    def add_user_message(self, message):
        """add a user message"""

    @abstractmethod
    def add_ai_message(self, message):
        """add a ai message"""

    @abstractmethod
    def clear(self):
        """clear all message"""


class ChatMessageHistory(BaseModel):
    messages: List[BaseMessage] = []
    conversation_id: str = ''

    def add_system_message(self, message: str) -> None:
        self.messages.append(SystemMessage(content=message))

    def add_user_message(self, message: str) -> None:
        self.messages.append(UserMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        self.messages.append(AssistantMessage(content=message))

    def clear(self) -> None:
        self.messages = []

    @property
    def listdict_message(self) -> List[dict]:
        listdict_message: List[dict] = []
        for message in self.messages:
            listdict_message.append({
                "role": message.type,
                "content": message.content
            })
        return listdict_message


def generate_conversation_id() -> str:
    """Generating a new conversation_id when a conversation initialize"""
    return str(int(time.time()))


def init_chat_message_history(system_content, user_content) -> ChatMessageHistory:
    messages = [
        SystemMessage(content=system_content),
        UserMessage(content=user_content),
    ]
    return ChatMessageHistory(messages=messages, conversation_id=generate_conversation_id())


class LLMPrompt(BaseModel):
    messages: List[BaseMessage]


class ListDictPrompt(BaseModel):
    """list dict type prompt. It can convert to ChatMessageHistory type."""
    messages: List[dict]

    @property
    def chat_message_history(self) -> ChatMessageHistory:
        message_history = ChatMessageHistory()
        for message in self.messages:
            role = message.get('role')
            content = message.get('content')
            if role == 'system':
                message_history.messages.append(SystemMessage(content=content))
            elif role == 'user':
                message_history.messages.append(UserMessage(content=content))
            elif role == 'assistant':
                message_history.messages.append(AssistantMessage(content=content))
        return message_history
