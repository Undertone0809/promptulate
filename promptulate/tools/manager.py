import json
from typing import Callable, List, Optional, Union

from promptulate.tools.base import BaseTool, Tool, ToolImpl, function_to_tool


class ToolManager:
    """ToolManager helps Agent to manage tools"""

    def __init__(self, tools: List[Union[BaseTool, Callable, Tool]]):
        self.tools: List[Tool] = []

        for tool in tools:
            if isinstance(tool, Callable):
                tool = function_to_tool(tool)
            elif isinstance(tool, BaseTool):
                tool = ToolImpl.from_base_tool(tool)

            self.tools.append(tool)

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Find specified tool by tool name."""
        return next((tool for tool in self.tools if tool.name == tool_name), None)

    def run_tool(self, tool_name: str, parameters: Union[str, dict]) -> str:
        """Run tool by input tool name and data inputs"""
        tool = self.get_tool(tool_name)

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
