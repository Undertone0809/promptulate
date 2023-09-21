from typing import List

from promptulate.tools.arxiv.tools import (
    ArxivSummaryTool,
    ArxivQueryTool,
    ArxivReferenceTool,
)
from promptulate.tools.base import BaseToolKit, Tool


class ArxivTootKit(BaseToolKit):
    def get_tools(self) -> List[Tool]:
        return [
            ArxivSummaryTool(),
            ArxivQueryTool(),
            ArxivReferenceTool(),
        ]
