import logging
from typing import List, Any, Optional

from promptulate.config import Config
from promptulate.tools.base import BaseTool

logger = logging.getLogger(__name__)
cfg = Config()


class ToolManager:
    """ToolManager helps ToolAgent manage tools"""

    def __init__(self, tools: List[BaseTool]):
        self.tools: List[BaseTool] = tools

    def find(self, tool_name: str) -> Optional[BaseTool]:
        """Find specified tool by tool name."""
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None

    def run_tool(self, tool_name: str, inputs: Any) -> str:
        """Run tool by input tool name and data inputs"""
        tool = self.find(tool_name)
        return tool.run(inputs)

    @property
    def tool_names(self) -> str:
        tool_names = ""
        for tool in self.tools:
            tool_names += f"{tool.name}, "
        return tool_names[:-2]

    @property
    def tool_descriptions(self) -> str:
        tool_descriptions = ""
        for tool in self.tools:
            tool_descriptions += f"{tool.name}: {tool.description}\n\n"
        return tool_descriptions
