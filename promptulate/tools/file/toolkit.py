import os
from typing import List, Literal, Optional

from promptulate.tools.base import BaseToolKit, ToolTypes
from promptulate.tools.file.tools import (
    AppendFileTool,
    CopyFileTool,
    DeleteFileTool,
    ListDirectoryTool,
    MoveFileTool,
    ReadFileTool,
    WriteFileTool,
)

FileToolType = Literal["write", "append", "read", "delete", "list", "copy", "move"]
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
        modes(Option): The modes of the file tool. Default is None.

    Returns:
        The instance object of the corresponding tool
    """

    def __init__(
        self,
        *,
        root_dir: Optional[str] = None,
        modes: Optional[List[FileToolType]] = None,
    ) -> None:
        self.root_dir = root_dir or os.getcwd()
        self.modes = modes or []

        for mode in self.modes:
            if mode not in TOOL_MAPPER.keys():
                raise ValueError(
                    f"{mode} does not exist.\n"
                    f"Please select from {list(TOOL_MAPPER.keys())}"
                )

    def get_tools(self) -> List[ToolTypes]:
        if self.modes:
            return [TOOL_MAPPER[mode](self.root_dir) for mode in self.modes]
        return [tool(self.root_dir) for tool in TOOL_MAPPER.values()]
