from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from promptulate.tools.arxiv.tools import (
        ArxivQueryTool,
        ArxivReferenceTool,
        ArxivSummaryTool,
    )
    from promptulate.tools.base import (
        BaseTool,
        Tool,
        define_tool,
        function_to_tool,
        function_to_tool_schema,
    )
    from promptulate.tools.duckduckgo.tools import (
        DuckDuckGoReferenceTool,
        DuckDuckGoTool,
        ddg_websearch,
    )
    from promptulate.tools.huggingface.tools import HuggingFaceTool
    from promptulate.tools.human_feedback import HumanFeedBackTool
    from promptulate.tools.iot_swith_mqtt import IotSwitchTool
    from promptulate.tools.langchain.tools import LangchainTool
    from promptulate.tools.math.tools import Calculator, calculator
    from promptulate.tools.paper.tools import PaperSummaryTool
    from promptulate.tools.python_repl import PythonREPLTool
    from promptulate.tools.semantic_scholar import (
        SemanticScholarCitationTool,
        SemanticScholarQueryTool,
        SemanticScholarReferenceTool,
    )
    from promptulate.tools.shell import ShellTool
    from promptulate.tools.sleep.tool import sleep_tool


def __getattr__(name):
    if name == "BaseTool":
        from promptulate.tools.base import BaseTool

        return BaseTool
    elif name == "Tool":
        from promptulate.tools.base import Tool

        return Tool
    elif name == "define_tool":
        from promptulate.tools.base import define_tool

        return define_tool
    elif name == "function_to_tool":
        from promptulate.tools.base import function_to_tool

        return function_to_tool
    elif name == "function_to_tool_schema":
        from promptulate.tools.base import function_to_tool_schema

        return function_to_tool_schema
    elif name == "ArxivQueryTool":
        from promptulate.tools.arxiv.tools import ArxivQueryTool

        return ArxivQueryTool
    elif name == "ArxivReferenceTool":
        from promptulate.tools.arxiv.tools import ArxivReferenceTool

        return ArxivReferenceTool
    elif name == "ArxivSummaryTool":
        from promptulate.tools.arxiv.tools import ArxivSummaryTool

        return ArxivSummaryTool
    elif name == "DuckDuckGoReferenceTool":
        from promptulate.tools.duckduckgo.tools import DuckDuckGoReferenceTool

        return DuckDuckGoReferenceTool
    elif name == "DuckDuckGoTool":
        from promptulate.tools.duckduckgo.tools import DuckDuckGoTool

        return DuckDuckGoTool
    elif name == "ddg_websearch":
        from promptulate.tools.duckduckgo.tools import ddg_websearch

        return ddg_websearch
    elif name == "SemanticScholarCitationTool":
        from promptulate.tools.semantic_scholar import SemanticScholarCitationTool

        return SemanticScholarCitationTool
    elif name == "SemanticScholarQueryTool":
        from promptulate.tools.semantic_scholar import SemanticScholarQueryTool

        return SemanticScholarQueryTool
    elif name == "SemanticScholarReferenceTool":
        from promptulate.tools.semantic_scholar import SemanticScholarReferenceTool

        return SemanticScholarReferenceTool
    elif name == "IotSwitchTool":
        from promptulate.tools.iot_swith_mqtt import IotSwitchTool

        return IotSwitchTool
    elif name == "HuggingFaceTool":
        from promptulate.tools.huggingface.tools import HuggingFaceTool

        return HuggingFaceTool
    elif name == "HumanFeedBackTool":
        from promptulate.tools.human_feedback import HumanFeedBackTool

        return HumanFeedBackTool
    elif name == "LangchainTool":
        from promptulate.tools.langchain.tools import LangchainTool

        return LangchainTool
    elif name == "Calculator":
        from promptulate.tools.math.tools import Calculator

        return Calculator
    elif name == "calculator":
        from promptulate.tools.math.tools import calculator

        return calculator
    elif name == "sleep_tool":
        from promptulate.tools.sleep.tool import sleep_tool

        return sleep_tool
    elif name == "PaperSummaryTool":
        from promptulate.tools.paper.tools import PaperSummaryTool

        return PaperSummaryTool
    elif name == "PythonREPLTool":
        from promptulate.tools.python_repl import PythonREPLTool

        return PythonREPLTool
    elif name == "ShellTool":
        from promptulate.tools.shell import ShellTool

        return ShellTool
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = [
    "BaseTool",
    "Tool",
    "define_tool",
    "function_to_tool",
    "function_to_tool_schema",
    "LangchainTool",
    "HuggingFaceTool",
    "DuckDuckGoReferenceTool",
    "DuckDuckGoTool",
    "ddg_websearch",
    "calculator",
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
    "sleep_tool",
    "HumanFeedBackTool",
]
