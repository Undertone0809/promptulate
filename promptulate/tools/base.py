import logging
import warnings
from abc import ABC, abstractmethod
from typing import List, Any, Callable

from pydantic import BaseModel, Extra

from promptulate.hook.base import Hook, HookTable

logger = logging.getLogger(__name__)


class BaseTool(ABC, BaseModel):
    """Interface tools must implement."""

    name: str
    """The unique name of the tool that clearly communicates its purpose."""
    description: str
    """Used to tell the model how/when/why to use the tool.
    You can provide few-shot examples as a part of the description."""
    few_shot_example: List[str] = None
    """Show how to use this tool. This is few shot for agent. You few shot may like:
    
    example1 = "Question: What is 37593 * 67?\n```\n37593 * 67\n```\nnumexpr.evaluate("37593 * 67")\nAnswer:2518731"
    example2 = "Question: What is 37593^(1/5)?\n```\n37593**(1/5)\n```\nnumexpr.evaluate("37593**(1/5)")\nAnswer:8.222831614237718"
    few_shot_example = [example1, example2]
    """

    # hook_manager: Optional[HookManager] = Field(default=HookManager())
    # """Hook manager will call hook function at the specified lifecycle."""

    def __init__(self, **kwargs):
        """Custom tool config.

        Args:
            **kwargs:
                hooks(List[Callable]): for adding to hook_manager
        """
        warnings.warn(
            "BaseTool is deprecated at v1.7.0. promptulate.tools.base.Tool is recommended.",
            DeprecationWarning,
        )
        super().__init__(**kwargs)
        if "hooks" in kwargs and kwargs["hooks"]:
            for hook in kwargs["hooks"]:
                Hook.mount_instance_hook(hook, self)
        Hook.call_hook(HookTable.ON_TOOL_CREATE, self, **kwargs)

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow

    def run(self, *args, **kwargs):
        """run the tool including specified function and hooks"""
        Hook.call_hook(HookTable.ON_TOOL_START, self, *args, **kwargs)
        result: Any = self._run(*args, **kwargs)
        logger.debug(f"[pne tool result] {result}")
        Hook.call_hook(HookTable.ON_TOOL_RESULT, self, result=result)
        return result

    @abstractmethod
    def _run(self, *args, **kwargs):
        """Run detail business, implemented by subclass."""


class Tool(ABC):
    name: str
    """Tool name"""
    description: str
    """Tool description"""

    def __init__(self, **kwargs):
        self.check_params()
        if "hooks" in kwargs and kwargs["hooks"]:
            for hook in kwargs["hooks"]:
                Hook.mount_instance_hook(hook, self)
        Hook.call_hook(HookTable.ON_TOOL_CREATE, self, **kwargs)

    def check_params(self):
        """Check parameters when initialization."""
        if not getattr(self, "name", None) or not getattr(self, "description", None):
            raise TypeError(
                f"{self.__class__.__name__} required parameters 'name' and 'description'."
            )

    def run(self, *args, **kwargs):
        """run the tool including specified function and hooks"""
        Hook.call_hook(HookTable.ON_TOOL_START, self, *args, **kwargs)
        result: Any = self._run(*args, **kwargs)
        logger.debug(f"[pne tool result] {result}")
        Hook.call_hook(HookTable.ON_TOOL_RESULT, self, result=result)
        return result

    @abstractmethod
    def _run(self, *args, **kwargs):
        """Run detail business, implemented by subclass."""


class ToolImpl(Tool):
    def __init__(self, name, description, callback: Callable, **kwargs):
        self.name = name
        self.description = description
        self.callback = callback

        super().__init__(**kwargs)

    def _run(self, *args, **kwargs):
        return self.callback(*args, **kwargs)


def define_tool(name: str, description: str, callback: Callable) -> ToolImpl:
    """
    A tool with llm or API wrapper will automatically initialize the llm and API wrapper classes,
    which can avoid this problem by initializing in this way.

    Args:
        name: tool name
        description: tool description
        callback: tool function when running

    Returns:
        A ToolImpl class (subclass of Tool).
    """

    return ToolImpl(name, description, callback)


class BaseToolKit:
    @abstractmethod
    def get_tools(self):
        """get tools in the toolkit"""
