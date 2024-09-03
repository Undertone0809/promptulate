def test_import_init():
    import promptulate as pne

    pne.ToolTypes  # noqa


def test_import_utils():
    from promptulate.utils import (
        StringTemplate,
        export_openai_key_pool,
        logger,
    )


def test_import_output_formatter():
    from promptulate.output_formatter import OutputFormatter


def test_import_promptulate():
    from promptulate import (
        AssistantMessage,
        BaseAgent,
        BaseLLM,
        BaseMessage,
        BaseTool,
        ChatOpenAI,
        MessageSet,
        SystemMessage,
        Tool,
        ToolAgent,
        UserMessage,
        WebAgent,
        chat,
        define_tool,
    )


def test_import_tools():
    from promptulate.tools import (
        ArxivQueryTool,
        ArxivReferenceTool,
        ArxivSummaryTool,
        BaseTool,
        Calculator,
        DuckDuckGoReferenceTool,
        DuckDuckGoTool,
        HuggingFaceTool,
        HumanFeedBackTool,
        IotSwitchTool,
        LangchainTool,
        PaperSummaryTool,
        PythonREPLTool,
        SemanticScholarCitationTool,
        SemanticScholarQueryTool,
        SemanticScholarReferenceTool,
        ShellTool,
        Tool,
        define_tool,
        function_to_tool,
        function_to_tool_schema,
        sleep_tool,
    )
