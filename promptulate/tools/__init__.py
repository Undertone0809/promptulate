from promptulate.tools.arxiv.tools import (
    ArxivQueryTool,
    ArxivSummaryTool,
    ArxivReferenceTool,
)
from promptulate.tools.base import BaseTool, Tool, define_tool
from promptulate.tools.duckduckgo.tools import DuckDuckGoTool, DuckDuckGoReferenceTool
from promptulate.tools.huggingface.tools import HuggingFaceTool
from promptulate.tools.human_feedback import HumanFeedBackTool
from promptulate.tools.iot_swith_mqtt import IotSwitchTool
from promptulate.tools.langchain.tools import LangchainTool
from promptulate.tools.math.tools import Calculator
from promptulate.tools.paper.tools import PaperSummaryTool
from promptulate.tools.python_repl import PythonREPLTool
from promptulate.tools.semantic_scholar import (
    SemanticScholarQueryTool,
    SemanticScholarReferenceTool,
    SemanticScholarCitationTool,
)
from promptulate.tools.shell import ShellTool

from promptulate.tools.sleep import SleepTool

__all__ = [
    "BaseTool",
    "Tool",
    "define_tool",
    "LangchainTool",
    "HuggingFaceTool",
    "DuckDuckGoReferenceTool",
    "DuckDuckGoTool",
    "PaperSummaryTool",
    "ArxivSummaryTool",
    "ArxivReferenceTool",
    "ArxivQueryTool",
    "SemanticScholarReferenceTool",
    "SemanticScholarCitationTool",
    "IotSwitchTool",
    "SemanticScholarQueryTool",
    "PythonREPLTool",
    "ShellTool",
    "Calculator",
    "SleepTool",
    "HumanFeedBackTool",
]
