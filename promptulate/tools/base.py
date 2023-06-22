from abc import ABC, abstractmethod
from pydantic import BaseModel


class BaseTool(ABC, BaseModel):
    """Interface tools must implement."""

    name: str
    """The unique name of the tool that clearly communicates its purpose."""
    description: str
    """Used to tell the model how/when/why to use the tool.
    You can provide few-shot examples as a part of the description.
    """

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class BaseToolKit:

    @abstractmethod
    def get_tools(self):
        """get tools in the toolkit"""
