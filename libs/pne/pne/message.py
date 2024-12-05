from abc import abstractmethod
from datetime import datetime
from typing import List, Optional, Union

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

    content: str

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


class MessageSet:
    def __init__(
        self,
        messages: List[BaseMessage],
        created_at: Optional[datetime] = None,
        metadata: Optional[dict] = None,
    ):
        self.messages: List[BaseMessage] = messages
        self.created_at: datetime = created_at or datetime.now()
        self.metadata: dict = metadata or {}

    @classmethod
    def from_listdict_data(
        cls, messages: List[dict], metadata: Optional[dict] = None
    ) -> "MessageSet":
        """Initialize MessageSet from a List[Dict] data

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
                    "function_call": msg.get("function_call"),
                    "tool_calls": msg.get("tool_calls"),
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
