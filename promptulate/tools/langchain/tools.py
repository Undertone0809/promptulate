from typing import TYPE_CHECKING, Any, List, Optional

from promptulate.pydantic_v1 import BaseModel
from promptulate.tools.base import Tool

if TYPE_CHECKING:
    from langchain.tools.base import BaseTool as LangchainBaseToolType


class LangchainTool(Tool):
    def __init__(self, langchain_tool: "LangchainBaseToolType", **kwargs):
        """Wrap langchain tool to promptulate tool.

        Args:
            langchain_tool(LangchainBaseToolType): Langchain tool.
        """
        from langchain.tools.base import BaseTool as LangchainBaseTool

        if not isinstance(langchain_tool, LangchainBaseTool):
            raise ValueError("langchain_tool should be type of langchain tool.")

        self.langchain_tool: "LangchainBaseToolType" = langchain_tool
        self.name: str = self.langchain_tool.name
        self.description: str = self.langchain_tool.description
        self.parameters: Optional[BaseModel] = self.langchain_tool.args_schema
        super().__init__(**kwargs)

    def _run(self, *args, **kwargs) -> Any:
        """Run the langchain tool.

        Args:
            *args: if the first arg is str, it will be used as tool_input.
            **kwargs: if the first arg is not str, it will be used as tool_input.

        Returns:
            Any: The result of the langchain tool.
        """
        if args and isinstance(args[0], str):
            return self.langchain_tool.run(tool_input=args[0])

        return self.langchain_tool.run(tool_input=kwargs)
