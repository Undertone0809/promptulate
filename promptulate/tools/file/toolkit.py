from typing import List, Optional
import os

from promptulate.tools.file.tools import (
    WriteFileTool,
    AppendFileTool,
    ReadFileTool,
    DeleteFileTool,
    ListDirectoryTool,
    CopyFileTool,
    MoveFileTool
)
from promptulate.tools.base import BaseToolKit, Tool

DefaultTools: List[Tool] = [
    WriteFileTool,
    AppendFileTool,
    ReadFileTool,
    DeleteFileTool,
    ListDirectoryTool,
    CopyFileTool,
    MoveFileTool
]

DefaultTools_str = {
    "WriteFileTool":WriteFileTool,
    "AppendFileTool":AppendFileTool,
    "ReadFileTool":ReadFileTool,
    "DeleteFileTool":DeleteFileTool,
    "ListDirectoryTool":ListDirectoryTool,
    "CopyFileTool":CopyFileTool,
    "MoveFileTool":MoveFileTool,
}


class FileToolKit(BaseToolKit):
    """File ToolKit
    
    Args:
        root_dir: The root directory of the file tool.
        selected_tools: The selected tools of the file tool.

    Returns:
        The instance object of the corresponding tool
    """

    def __init__(self, root_dir: str = None,selected_tools: Optional[List[str]] = None) -> None:
        if root_dir is None or root_dir == "":
            root_dir = os.getcwd()
        self.root_dir = root_dir
        self.selected_tools = selected_tools

    def get_tools(self) -> List[Tool]:
        tools_list = []

        if self.selected_tools is None or self.selected_tools == []:
            tools = DefaultTools_str
        else:
            tools = self.selected_tools
        for tool in tools:
            tool_cls = DefaultTools_str[tool]
            tools_list.append(tool_cls(self.root_dir))
        return tools_list

    