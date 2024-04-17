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

TOOL_MAPPER = {
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
        self.root_dir = root_dir or os.getcwd()
        self.modes = modes or []

        for mode in self.modes:
            if mode not in TOOL_MAPPER.keys():
                raise ValueError(
                    f"{mode} does not exist.\n"
                    f"Please select from {list(TOOL_MAPPER.keys())}"
                )

    def get_tools(self) -> List[Tool]:
        if self.modes:
            return [TOOL_MAPPER[mode](self.root_dir) for mode in self.modes]
        return [tool(self.root_dir) for tool in TOOL_MAPPER.values()]
