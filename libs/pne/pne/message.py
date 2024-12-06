from abc import abstractmethod
from datetime import datetime
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

from pydantic import BaseModel, Field


class BaseMessage(BaseModel):
    """Message basic object.

    Args:
        content (str): message content
        additional_kwargs (dict): additional kwargs
        created_at (datetime): created at time
    """

    content: Union[str, list[Union[str, dict]]]
    additional_kwargs: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    @abstractmethod
    def type(self) -> str:
        """Type of the message, used for serialization."""


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

    function_call: Optional[dict] = None
    tool_calls: Optional[List[dict]] = None

    @property
    def type(self) -> str:
        return "assistant"


class FunctionMessage(BaseMessage):
    """Type of message that is a function message. Currently used in OpenAI.

    Args:
        content (str): The content/result of the function call
        name (str): The name of the function that was called
        arguments (Optional[Union[str, dict]]): The arguments passed to the function
        status (Optional[str]): Status of the function call (e.g., "success", "error")
    """

    name: str
    arguments: Optional[Union[str, dict]] = None
    status: Optional[str] = "success"

    @property
    def type(self) -> str:
        return "function"


class ToolMessage(BaseMessage):
    """Type of message that is a tool message. Currently used in OpenAI.

    Args:
        content (str): The content/result of the tool call
        name (str): The name of the tool that was called
        tool_call_id (str): The ID of the tool call this message is responding to
        arguments (Optional[Union[str, dict]]): The arguments passed to the tool
        status (Optional[str]): Status of the tool call (e.g., "success", "error")
    """

    name: str
    tool_call_id: str
    arguments: Optional[Union[str, dict]] = None
    status: Optional[str] = "success"

    @property
    def type(self) -> str:
        return "tool"


class StreamMessageIterator:
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


class MessageSet:
    def __init__(
        self,
        messages: List[BaseMessage],
        created_at: Optional[datetime] = None,
        metadata: Optional[Dict] = None,
    ):
        self.messages: List[BaseMessage] = messages
        self.created_at: datetime = created_at or datetime.now()
        self.metadata: Dict = metadata or {}

    @classmethod
    def from_raw(
        cls, messages: List[Dict], metadata: Optional[Dict] = None
    ) -> "MessageSet":
        """Initialize MessageSet from a list[dict[str, any]] data

        Args:
            messages (List[Dict]): List of message dictionaries. Example:
            messages = [
                {"role": "user", "content": "What's the weather?"},
                {
                    "role": "assistant",
                    "content": "Let me check the weather.",
                    "function_call": {"name": "get_weather", "arguments": '{"location": "London"}'}
                },
                {
                    "role": "function",
                    "name": "get_weather",
                    "content": "The weather in London is sunny and 22°C"
                }
            ]
            metadata (Optional[dict]): Additional metadata for the message set

        Returns:
            MessageSet: Initialized MessageSet instance
        """  # noqa
        type_map = {
            "completion": CompletionMessage,
            "system": SystemMessage,
            "user": UserMessage,
            "assistant": AssistantMessage,
            "function": FunctionMessage,
            "tool": ToolMessage,
        }

        processed_messages: List[BaseMessage] = []
        for msg in messages:
            role = msg["role"]
            message_class = type_map[role]

            if role == "assistant":
                kwargs = {
                    "content": msg["content"],
                    "function_call": msg.get("function_call", {}),
                    "tool_calls": msg.get("tool_calls", []),
                }
            elif role in ["function", "tool"]:
                kwargs = {
                    "content": msg["content"],
                    "name": msg["name"],
                }
                if role == "function":
                    kwargs["arguments"] = msg.get("arguments")
                    kwargs["status"] = msg.get("status", "success")
                else:
                    kwargs["tool_call_id"] = msg["tool_call_id"]
                    kwargs["arguments"] = msg.get("arguments")
                    kwargs["status"] = msg.get("status", "success")
            else:
                kwargs = {"content": msg["content"]}

            processed_messages.append(message_class(**kwargs))

        return cls(messages=processed_messages, metadata=metadata)

    def to_raw(self) -> List[Dict[str, Any]]:
        return [
            {
                "role": message.type,
                "content": message.content,
                "function_call": message.function_call
                if isinstance(message, AssistantMessage)
                else None,
                "tool_calls": message.tool_calls
                if isinstance(message, AssistantMessage)
                else None,
            }
            for message in self.messages
        ]
