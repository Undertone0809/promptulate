import os
from typing import List, Optional

from promptulate.tools.base import BaseToolKit, Tool
from promptulate.tools.file.tools import (
    AppendFileTool,
    CopyFileTool,
    DeleteFileTool,
    ListDirectoryTool,
    MoveFileTool,
    ReadFileTool,
    WriteFileTool,
)

DefaultTools: List[Tool] = [
    WriteFileTool,
    AppendFileTool,
    ReadFileTool,
    DeleteFileTool,
    ListDirectoryTool,
    CopyFileTool,
    MoveFileTool,
]

DefaultTools_str = {
    "write": WriteFileTool,
    "append": AppendFileTool,
    "read": ReadFileTool,
    "delete": DeleteFileTool,
    "list": ListDirectoryTool,
    "copy": CopyFileTool,
    "move": MoveFileTool,
}


class FileToolKit(BaseToolKit):
    """File ToolKit

    Args:
        root_dir: The root directory of the file tool.
        selected_tools: The selected tools of the file tool.

    Returns:
        The instance object of the corresponding tool
    """

    def __init__(self, root_dir: str = None, modes: Optional[List[str]] = None) -> None:
        """validate_root_dir"""
        if root_dir is None or root_dir == "":
            root_dir = os.getcwd()
        self.root_dir = root_dir
        """validate_tools"""
        if modes is not None and modes != []:
            for tool in modes:
                if tool not in DefaultTools_str:
                    raise ValueError(
                        f"{tool} does not exist.\n"
                        f"Please select from {list(DefaultTools_str.keys())}"
                    )
        self.modes = modes

    def get_tools(self) -> List[Tool]:
        tools_list = []

        if self.modes is None or self.modes == []:
            tools = DefaultTools_str
        else:
            tools = self.modes
        for tool in tools:
            tool_cls = DefaultTools_str[tool]
            tools_list.append(tool_cls(self.root_dir))
        return tools_list
