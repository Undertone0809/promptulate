from typing import List
from abc import abstractmethod
from pydantic import BaseModel, Field
from promptulate.utils import generate_conversation_id

__all__ = [
    "BaseMessage",
    "BaseChatMessageHistory",
    "SystemMessage",
    "UserMessage",
    "AssistantMessage",
    "ChatMessageHistory",
    "LLMPrompt",
    "ListDictPrompt",
    "init_chat_message_history",
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
    conversation_id: str = ""

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
            listdict_message.append({"role": message.type, "content": message.content})
        return listdict_message


def init_chat_message_history(system_content, user_content) -> ChatMessageHistory:
    messages = [
        SystemMessage(content=system_content),
        UserMessage(content=user_content),
    ]
    return ChatMessageHistory(
        messages=messages, conversation_id=generate_conversation_id()
    )


class LLMPrompt(BaseModel):
    messages: List[BaseMessage]


class ListDictPrompt(BaseModel):
    """list dict type prompt. It can convert to ChatMessageHistory type."""

    messages: List[dict]

    @property
    def chat_message_history(self) -> ChatMessageHistory:
        message_history = ChatMessageHistory()
        for message in self.messages:
            role = message.get("role")
            content = message.get("content")
            if role == "system":
                message_history.messages.append(SystemMessage(content=content))
            elif role == "user":
                message_history.messages.append(UserMessage(content=content))
            elif role == "assistant":
                message_history.messages.append(AssistantMessage(content=content))
        return message_history
