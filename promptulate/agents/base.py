from abc import ABC, abstractmethod
from typing import List, Callable

from promptulate.hook import Hook, HookTable


class BaseAgent(ABC):
    """Base class of Agent."""

    def __init__(self, hooks: List[Callable] = None, *args, **kwargs):
        if hooks:
            for hook in hooks:
                Hook.mount_instance_hook(hook, self)
        Hook.call_hook(HookTable.ON_AGENT_CREATE, self, *args, **kwargs)

    def run(self, *args, **kwargs):
        """run the tool including specified function and hooks"""
        Hook.call_hook(HookTable.ON_AGENT_START, self, *args, **kwargs)
        result: str = self._run(*args, **kwargs)
        Hook.call_hook(HookTable.ON_AGENT_RESULT, self, result=result)
        return result

    @abstractmethod
    def _run(self, *args, **kwargs) -> str:
        """Run the detail agent, implemented by subclass."""
