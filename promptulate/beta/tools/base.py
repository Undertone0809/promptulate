from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


class BaseTool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, *args, **kwargs): ...


class BaseToolKit(ABC):
    @abstractmethod
    def get_tools(self) -> List[BaseTool]: ...
