import warnings
from abc import abstractmethod
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

from promptulate.pydantic_v1 import BaseModel, Field

__all__ = [
    "LLMType",
    "BaseMessage",
    "CompletionMessage",
    "SystemMessage",
    "UserMessage",
    "AssistantMessage",
    "MessageSet",
    "init_chat_message_history",
    "StreamIterator",
]


class BaseMessage(BaseModel):
    """Message basic object."""

    content: str
    additional_kwargs: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

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
        additional_kwargs: Optional dictionary with additional keyword parameters
        content: An optional string that represents the content
    """

    def __init__(
        self,
        response_stream,
        parse_content: Callable[[Any], Tuple[Optional[str], Dict[str, Any]]],
        return_raw_response: bool = False,
        additional_kwargs: Optional[Dict[str, Any]] = None,
        content: Optional[str] = None,
    ):
        """
        The constructor for BaseStreamIterator class.

        Args:
            response_stream: The stream of responses from the LLM model.
            parse_content: The callback function to parse the chunk.
            return_raw_response: A boolean indicating whether to return the raw response
            or not.
            additional_kwargs: Optional dictionary with additional keyword parameters
            content: An optional string that represents the content
        """
        self.response_stream = response_stream
        self.return_raw_response = return_raw_response
        self.parse_content = parse_content
        self.additional_kwargs = additional_kwargs or {}
        self.content = content

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

        Args:
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
            content, ret_data = self.parse_content(chunk)
            if content is None:
                continue
            if self.return_raw_response:
                additional_kwargs: dict = ret_data
                message = AssistantMessage(
                    content=content,
                    additional_kwargs=additional_kwargs,
                )
                return message

            return content

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



class LLMType(str, Enum):
    """All LLM type here"""

    OpenAI = auto()
    ChatOpenAI = auto()
    ErnieBot = auto()
    QianFan = auto()
    ZhiPu = auto()


class MessageSet:
    """MessageSet can be used in Memory, LLMs, Framework and some else.
    It's a universal chat message format in promptulate.
    """

    def __init__(
        self,
        messages: List[BaseMessage],
        conversation_id: Optional[str] = None,
        additional_kwargs: Optional[dict] = None,
    ):
        self.messages: List[BaseMessage] = messages
        self.conversation_id: Optional[str] = conversation_id
        self.additional_kwargs: dict = additional_kwargs or {}
        self.created_at: datetime = datetime.now()

        if conversation_id:
            # show tip, this will be deprecated in v1.9.0
            warnings.warn(
                "The parameter 'conversation_id' is deprecated and will be removed in version 1.9.0.",  # noqa
                DeprecationWarning,
                stacklevel=2,
            )

    @classmethod
    def from_listdict_data(
        cls, value: List[Dict], additional_kwargs: Optional[dict] = None
    ) -> "MessageSet":
        """initialize MessageSet from a List[Dict] data

        Args:
            value(List[Dict]): the example is as follows:
                [
                    {"type": "user", "content": "This is a message1."},
                    {"type": "assistant", "content": "This is a message2."}
                ]
            additional_kwargs(Optional[dict]): additional kwargs

        Returns:
            initialized MessageSet
        """
        type_map = {
            "completion": CompletionMessage,
            "system": SystemMessage,
            "user": UserMessage,
            "assistant": AssistantMessage,
        }

        messages: List[BaseMessage] = [
            type_map[item["role"]](content=item["content"]) for item in value
        ]
        return cls(messages=messages, additional_kwargs=additional_kwargs)

    @property
    def listdict_messages(self) -> List[Dict[str, str]]:
        """Convert the MessageSet messages to a list of dictionary(openai type).

        Returns:
            List[Dict[str, str]]: the example is as follows:
                [
                    {"role": "user", "content": "This is a message1."},
                    {"role": "assistant", "content": "This is a message2."}
                ]
        """
        converted_messages = []
        for message in self.messages:
            converted_messages.append(
                {"role": message.type, "content": message.content}
            )
        return converted_messages

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

    def add_ai_message(self, message: Union[str, BaseModel]) -> None:
        """Add a message from an AI model. If the message has a model_dump method, which
        means it's a pydantic model, it will be dumped to a string and added to the
        message set. Otherwise, it will be added as a string.

        Args:
            message(str | BaseModel): The message from the AI model.

        Returns:
            None
        """
        if hasattr(message, "model_dump"):
            _: dict = message.model_dump()
            self.messages.append(AssistantMessage(content=str(_), additional_kwargs=_))
            return

        self.messages.append(AssistantMessage(content=message))

    def add_from_message_set(self, message_set: "MessageSet") -> None:
        """Add messages from another message.
        Args:
            message_set:

        Returns:
            None
        """
        self.messages.extend(message_set.messages)
