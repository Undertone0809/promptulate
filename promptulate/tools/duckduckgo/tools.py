import time
from typing import Dict, List, Union

from promptulate.tools.base import Tool
from promptulate.tools.duckduckgo.api_wrapper import DuckDuckGoSearchAPIWrapper
from promptulate.utils.core_utils import listdict_to_string


class DuckDuckGoTool(Tool):
    """Tool that adds the capability to query the DuckDuckGo search API."""

    name: str = "ddg-search"
    description: str = (
        "A wrapper around DuckDuckgo Web Search. "
        "Useful for when you need to answer questions about current events. "
        "Args : keyword(str)"
        "Input should be a search query."
    )
    api_wrapper: DuckDuckGoSearchAPIWrapper = DuckDuckGoSearchAPIWrapper()
    max_retry: int = 5

    def _run(self, keyword: str, **kwargs) -> Union[str, List[str]]:
        """Run duckduckgo search and get search result.

        Args:
            keyword: query keyword
            **kwargs:
                result_type(Optional[str]) - default return string type data. Return
                List[str] type data.
                if you pass result_type="original"

        Returns:
            default is string. Return List[str] type data if you pass
            result_type="original"
        """
        from duckduckgo_search.exceptions import RateLimitException

        attempt = 0
        while attempt < self.max_retry:
            try:
                result = self.api_wrapper.query(keyword, **kwargs)
                if "result_type" in kwargs and kwargs["result_type"] == "original":
                    return result
                return " ".join(result)
            except RateLimitException as e:
                attempt += 1

                if attempt >= self.max_retry:
                    raise e

                time.sleep(1.3**attempt)  # Exponential backoff
            except Exception as e:
                raise e


class DuckDuckGoReferenceTool(Tool):
    """Tool that adds the capability to query the DuckDuckGo search API. Compared to
    DuckDuckGoTool, this tool can return references information like href, title.
    """

    name: str = "ddg-search-with-references"
    description: str = (
        "A wrapper around DuckDuckGo Search, it returns query result and references url"
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    api_wrapper: DuckDuckGoSearchAPIWrapper = DuckDuckGoSearchAPIWrapper()

    def _run(self, keyword: str, **kwargs) -> Union[str, List[Dict[str, str]]]:
        """Run duckduckgo search and get search result with href, snippet, title.

        Args:
            keyword: query keyword
            **kwargs:
                result_type(Optional[str]) - default return string type data. Return
                List[str] type data.
                if you pass result_type="original"

        Returns:
            default is string. Return List[Dict[str, str]] type data if you pass
            result_type="original"
        """
        result = self.api_wrapper.query_by_formatted_results(keyword, **kwargs)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result, item_suffix="\n")


def ddg_websearch(query: str) -> str:
    """Run duckduckgo search and get search result.

    Args:
        query: query keyword
    """
    tool = DuckDuckGoTool()
    return tool.run(query)
