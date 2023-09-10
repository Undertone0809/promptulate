from promptulate.tools.base import Tool


class LangchainTool(Tool):
    def __init__(self, langchain_tool, **kwargs):
        from langchain.tools.base import BaseTool as LangchainBaseTool

        if not isinstance(langchain_tool, LangchainBaseTool):
            raise ValueError("langchain_tool should be type of langchain tool.")

        self.langchain_tool = langchain_tool
        self.name = self.langchain_tool.name
        self.description = self.langchain_tool.description
        super().__init__(**kwargs)

    def _run(self, *args, **kwargs):
        return self.langchain_tool.run(*args, **kwargs)
