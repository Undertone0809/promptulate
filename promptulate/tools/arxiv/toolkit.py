from typing import List

from promptulate.tools.base import BaseToolKit, BaseTool
from promptulate.tools.arxiv.tools import ArxivSummaryTool, ArxivQueryTool, ArxivReferenceTool


class ArxivTootKit(BaseToolKit):

    def get_tools(self) -> List[BaseTool]:
        return [
            ArxivSummaryTool(),
            ArxivQueryTool(),
            ArxivReferenceTool(),
        ]
