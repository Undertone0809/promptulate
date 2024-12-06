"""
TODO: chat use response_format not output_schema
"""

from enum import Enum, auto
from typing import List, Optional

from pydantic import BaseModel

from pne.llm.base import LLM
from pne.tools.base import ToolTypes


class Mode(Enum):
    CHAT = auto()
    REACT = auto()
    PLANED_REACT = auto()
    PLANED_REACT_WITHOUT_REEDBACK = auto()
    TOOL = auto()


class AIChat:
    def __init__(
        self,
        model: Optional[str] = None,
        model_config: Optional[dict] = None,
        tools: Optional[List[ToolTypes]] = None,
        custom_llm: Optional[LLM] = None,
        enable_plan: bool = False,
        enable_memory: bool = False,
        mode: Mode = Mode.CHAT,
        callbacks: Optional[List] = None,
    ):
        pass

    def chat(self, *args, **kwargs):
        pass

    def bind_tools(self, tools: List[ToolTypes], *args, **kwargs):
        pass

    @classmethod
    def from_chat(cls, *args, **kwargs) -> "AIChat":
        pass


def chat(messages, *args, **kwargs):
    ai = AIChat.from_chat(*args, **kwargs)
    return ai.run(messages)
