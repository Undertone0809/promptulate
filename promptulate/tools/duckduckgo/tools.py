from pydantic import Field
from typing import List, Union, Dict

from promptulate.tools.base import BaseTool
from promptulate.utils.core_utils import listdict_to_string
from promptulate.tools.duckduckgo.api_wrapper import DuckDuckGoSearchAPIWrapper


class DuckDuckGoTool(BaseTool):
    """Tool that adds the capability to query the DuckDuckGo search API."""
    name = "ddg-search"
    description = (
        "A wrapper around DuckDuckGo Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    api_wrapper: DuckDuckGoSearchAPIWrapper = Field(default_factory=DuckDuckGoSearchAPIWrapper)

    def run(self, keyword: str, **kwargs) -> Union[str, List[str]]:
        """Run duckduckgo search and get search result.

        Args:
            keyword: query keyword
            **kwargs:
                result_type(Optional[str]) - default return string type data. Return List[str] type data
                if you pass result_type="original"

        Returns:
            default is string. Return List[str] type data if you pass result_type="original"
        """
        result = self.api_wrapper.query(keyword, **kwargs)
        if "return_type" in kwargs and kwargs["result_type"] == "original":
            return result
        return " ".join(result)


class DuckDuckGoReferenceTool(BaseTool):
    """Tool that adds the capability to query the DuckDuckGo search API. Compared to DuckDuckGoTool, this
    tool can return references information like href, title.
    """
    name = "ddg-search-with-references"
    description = ""
    api_wrapper: DuckDuckGoSearchAPIWrapper = Field(default_factory=DuckDuckGoSearchAPIWrapper)

    def run(self, keyword: str, **kwargs) -> Union[str, List[Dict[str, str]]]:
        """Run duckduckgo search and get search result with href, snippet, title.

        Args:
            keyword: query keyword
            **kwargs:
                result_type(Optional[str]) - default return string type data. Return List[str] type data
                if you pass result_type="original"

        Returns:
            default is string. Return List[Dict[str, str]] type data if you pass result_type="original"
        """
        result = self.api_wrapper.query_by_formatted_results(keyword, **kwargs)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result, item_suffix="\n")
