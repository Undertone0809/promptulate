import json
from typing import Callable, List, Optional, Union

from promptulate.tools.base import BaseTool, Tool, ToolImpl, function_to_tool


class ToolManager:
    """ToolManager helps ToolAgent manage tools"""

    def __init__(self, tools: List[Union[BaseTool, Callable, Tool]]):
        self.tools: List[Union[BaseTool, Callable, Tool]] = []

        for tool in tools:
            if isinstance(tool, Callable):
                tool = function_to_tool(tool)

            self.tools.append(tool)

    def find(self, tool_name: str) -> Optional[BaseTool]:
        """Find specified tool by tool name."""
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None

    def run_tool(self, tool_name: str, parameters: Union[str, dict]) -> str:
        """Run tool by input tool name and data inputs"""
        tool = self.find(tool_name)

        if tool is None:
            return (
                f"{tool_name} has not been provided yet, please use the provided tool."
            )

        if isinstance(parameters, dict):
            return tool.run(**parameters)
        else:
            return tool.run(parameters)

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
            tool_descriptions += json.dumps(tool.to_schema()) + "\n"
        return tool_descriptions

    def func(self):
        pass
