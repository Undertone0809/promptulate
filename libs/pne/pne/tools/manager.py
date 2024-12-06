import inspect
import json
from typing import Any, Callable, Dict, List, Optional, Union

from pne.tools.base import Tool, ToolKit, ToolTypes


class ToolManager:
    """ToolManager helps Agent to manage tools"""

    def __init__(self, tools: List[ToolTypes]):
        self.tools: Dict[str, Tool] = {}

        for tool in tools:
            self._register_tool(tool)

    def _register_tool(self, tool: ToolTypes) -> None:
        """Register a single tool, which could be:
        - A ToolKit containing multiple tools
        - A single Tool instance
        - A function or method from which a Tool can be derived

        Args:
            tool: The tool to be registered
        """
        if isinstance(tool, ToolKit):
            self.tools.update(tool.tools)
        elif isinstance(tool, Tool):
            self.tools[tool.name] = tool
        elif inspect.isfunction(tool) or inspect.ismethod(tool):
            t = Tool.from_function(tool)
            self.tools[t.name] = t
        else:
            raise ValueError(f"[pne tool manager] Unknown tool type {tool}.")

    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Find specified tool by tool name."""
        return self.tools.get(tool_name)

    def run_tool(self, tool_name: str, parameters: Union[str, dict]) -> str:
        """Run tool by input tool name and parameters."""
        tool = self.get_tool(tool_name)
        if tool is None:
            return (
                f"{tool_name} has not been provided yet, please use the provided tool."
            )

        if isinstance(parameters, dict):
            return tool.run(**parameters)
        return tool.run(parameters)

    def add_tool(self, tool: ToolTypes) -> None:
        self._register_tool(tool)

    @property
    def tool_names(self) -> str:
        """Get all tool names."""
        return ", ".join(self.tools.keys())

    @property
    def tool_descriptions(self) -> str:
        """Get all tool descriptions, including the schema if available."""
        return "\n".join(json.dumps(t.to_function_call()) for t in self.tools.values())

    @property
    def tool_call_schemas(self) -> List[Dict[str, Any]]:
        """Get all tool call schemas."""
        return [t.to_tool_call_schema() for t in self.tools.values()]

    @property
    def function_call_schemas(self) -> List[Dict[str, Any]]:
        """Get all function call schemas."""
        return [t.to_function_call() for t in self.tools.values()]
