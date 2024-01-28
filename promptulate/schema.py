from abc import abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, Iterator, List, Optional, Union

from pydantic import BaseModel, Field

__all__ = [
    "LLMType",
    "BaseMessage",
    "CompletionMessage",
    "SystemMessage",
    "UserMessage",
    "AssistantMessage",
    "MessageSet",
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


class StreamIterator:
    """
    This class is an iterator for the response stream from the LLM model.

    Attributes:
        response_stream: The stream of responses from the LLM model.
        parse_content: The callback function to parse the chunk.
        return_raw_response: A boolean indicating whether to return the raw response
        or not.
    """

    def __init__(
        self,
        response_stream,
        parse_content: callable([[Any], [str, str]]),
        return_raw_response: bool = False,
    ):
        """
        The constructor for BaseStreamIterator class.

        Parameters:
            response_stream: The stream of responses from the LLM model.
            return_raw_response (bool): A flag indicating whether to return the raw
            response or not.
        """
        self.response_stream = response_stream
        self.return_raw_response = return_raw_response
        self.parse_content = parse_content

    def __iter__(self) -> Union[Iterator[BaseMessage], Iterator[str]]:
        """
        The iterator method for the BaseStreamIterator class.

        Returns:
            self: An instance of the BaseStreamIterator class.
        """
        return self

    def parse_chunk(self, chunk) -> Optional[Union[str, BaseMessage]]:
        """
        This method is used to parse a chunk from the response stream. It returns
        None if the chunk is empty, otherwise it returns the parsed chunk.

        Parameters:
            chunk: The chunk to be parsed.

        Returns:
            Optional: The parsed chunk or None if the chunk is empty.
        """
        content, ret_data = self.parse_content(chunk)
        if content is None:
            return None
        if self.return_raw_response:
            additional_kwargs: dict = ret_data
            message = AssistantMessage(
                content=content,
                additional_kwargs=additional_kwargs,
            )
            return message

        return content

    def __next__(self) -> Union[str, BaseMessage]:
        """
        The next method for the BaseStreamIterator class.

        This method is used to get the next response from the LLM model. It iterates
        over the response stream and parses each chunk using the parse_chunk method.
        If the parsed chunk is not None, it returns the parsed chunk as the next
        response. If there are no more messages in the response stream, it raises a
        StopIteration exception.

        Returns:
            Union[str, BaseMessage]: The next response from the LLM model. If
            return_raw_response is True, it returns an AssistantMessage instance,
            otherwise it returns the content of the response as a string.
        """
        for chunk in self.response_stream:
            message = self.parse_chunk(chunk)
            if message is not None:
                return message

        # If there are no more messages, stop the iteration
        raise StopIteration


class CompletionMessage(BaseMessage):
    """Type of completion message. Used in OpenAI currently"""

    @property
    def type(self) -> str:
        return "completion"


class SystemMessage(BaseMessage):
    """Type of message that is a system message. Currently used in OpenAI."""

    @property
    def type(self) -> str:
        """Type of the message, used for serialization."""
        return "system"


class UserMessage(BaseMessage):
    """Type of message that is a user message. Currently used in OpenAI."""

    @property
    def type(self) -> str:
        return "user"


class AssistantMessage(BaseMessage):
    """Type of message that is an assistant message. Currently used in OpenAI."""

    @property
    def type(self) -> str:
        return "assistant"


MESSAGE_TYPE = {
    "completion": CompletionMessage,
    "system": SystemMessage,
    "user": UserMessage,
    "assistant": AssistantMessage,
}


class LLMType(str, Enum):
    """All LLM type here"""

    OpenAI = "OpenAI"
    ChatOpenAI = "ChatOpenAI"
    ErnieBot = "ErnieBot"
    QianFan = "QianFan"
    ZhiPu = "ZhiPu"


class MessageSet:
    """MessageSet can be used in Memory, LLMs, Framework and some else.
    It's a universal chat message format in promptulate.
    """

    def __init__(
        self, messages: List[BaseMessage], conversation_id: Optional[str] = None
    ):
        self.messages: List[BaseMessage] = messages
        self.conversation_id: Optional[str] = conversation_id

    @classmethod
    def from_listdict_data(cls, value: List[Dict]) -> "MessageSet":
        """initialize MessageSet from a List[Dict] data

        Args:
            value(List[Dict]): the example is as follow:
                [
                    {"type": "user", "content": "This is a message1."},
                    {"type": "assistant", "content": "This is a message2."}
                ]

        Returns:
            initialized MessageSet
        """
        messages: List[BaseMessage] = [
            MESSAGE_TYPE[item["role"]](content=item["content"]) for item in value
        ]
        return cls(messages=messages)

    @property
    def listdict_messages(self) -> List[Dict]:
        converted_messages = []
        for message in self.messages:
            converted_messages.append(
                {"role": message.type, "content": message.content}
            )
        return converted_messages

    @property
    def memory_messages(self) -> List[Dict]:
        return self.listdict_messages

    def to_llm_prompt(self, llm_type: LLMType) -> Any:
        """Convert the MessageSet messages to specified llm prompt"""
        if not llm_type:
            ValueError(
                "Missing llm_type, llm_type is needed if you want to use llm_prompt."
            )
        return _to_llm_prompt[llm_type](self)

    @property
    def string_messages(self) -> str:
        """Convert the message to a string type, it can be used as a prompt for OpenAI
        completion."""
        string_result = ""
        for message in self.messages:
            string_result += f"{message.content}\n"
        return string_result

    def add_message(self, message: BaseMessage) -> None:
        self.messages.append(message)

    def add_completion_message(self, message: str) -> None:
        self.messages.append(CompletionMessage(content=message))

    def add_system_message(self, message: str) -> None:
        self.messages.append(SystemMessage(content=message))

    def add_user_message(self, message: str) -> None:
        self.messages.append(UserMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        self.messages.append(AssistantMessage(content=message))


def init_chat_message_history(
    system_content: str, user_content: str, llm: LLMType
) -> MessageSet:
    if llm == llm.ChatOpenAI or llm == llm.OpenAI:
        messages = [
            SystemMessage(content=system_content),
            UserMessage(content=user_content),
        ]
    else:
        messages = [
            UserMessage(content=system_content),
            AssistantMessage(content="好的"),
            UserMessage(content=user_content),
        ]
    return MessageSet(messages=messages)


def _to_openai_llm_prompt(message_set: MessageSet) -> str:
    return message_set.string_messages


def _to_chat_openai_llm_prompt(message_set: MessageSet) -> List[Dict]:
    return message_set.listdict_messages


def _to_ernie_bot_llm_prompt(message_set: MessageSet) -> List[Dict]:
    return message_set.listdict_messages


def _to_qian_fan_llm_prompt(message_set: MessageSet) -> List[Dict]:
    return message_set.listdict_messages


def _to_zhipu_llm_prompt(message_set: MessageSet) -> List[Dict]:
    return message_set.listdict_messages


_to_llm_prompt: Dict[LLMType, Callable] = {
    LLMType.OpenAI: _to_openai_llm_prompt,
    LLMType.ChatOpenAI: _to_chat_openai_llm_prompt,
    LLMType.ErnieBot: _to_ernie_bot_llm_prompt,
    LLMType.QianFan: _to_qian_fan_llm_prompt,
    LLMType.ZhiPu: _to_zhipu_llm_prompt,
}
