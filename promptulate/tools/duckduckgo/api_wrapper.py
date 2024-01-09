from typing import Dict, List, Optional

from pydantic import BaseModel, Extra
from pydantic.class_validators import root_validator


class DuckDuckGoSearchAPIWrapper(BaseModel):
    """Wrapper for DuckDuckGo Search API. Free and does not require any setup."""

    region: Optional[str] = "us-en"
    safe_search: str = "moderate"
    time: Optional[str] = "y"
    max_num_of_results: int = 5

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator(skip_on_failure=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that python package exists in environment."""
        try:
            from duckduckgo_search import DDGS  # noqa
        except ImportError:
            raise ValueError(
                "Could not import duckduckgo-search python package. "
                "Please install it with `pip install duckduckgo-search`."
            )
        return values

    def query(
        self, keyword: str, num_results: Optional[int] = None, **kwargs
    ) -> List[str]:
        """Run query through DuckDuckGo and return concatenated results."""
        from duckduckgo_search import DDGS

        if not num_results:
            num_results = self.max_num_of_results

        with DDGS() as ddgs:
            results = ddgs.text(
                keyword,
                region=self.region,
                safesearch=self.safe_search,
                timelimit=self.time,
            )
            if results is None or next(results, None) is None:
                return ["No good DuckDuckGo Search Result was found"]

            snippets = []
            for i, result in enumerate(results, 1):
                snippets.append(result["body"])
                if i == num_results:
                    break
            return snippets

    def query_by_formatted_results(
        self, query: str, num_results: Optional[int] = None, **kwargs
    ) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo and return metadata.

        Args:
            query: The query to search for.
            num_results: The number of results to return.

        Returns:
            A list of dictionaries with the following keys:
                snippet - The description of the result.
                title - The title of the result.
                link - The link to the result.
        """
        from duckduckgo_search import DDGS

        if not num_results:
            num_results = self.max_num_of_results

        with DDGS() as ddgs:
            results = ddgs.text(
                query,
                region=self.region,
                safesearch=self.safe_search,
                timelimit=self.time,
            )
            if results is None or next(results, None) is None:
                return [{"Result": "No good DuckDuckGo Search Result was found"}]

            def to_metadata(result: Dict) -> Dict[str, str]:
                return {
                    "title": result["title"],
                    "snippet": result["body"],
                    "link": result["href"],
                }

            formatted_results = []
            for i, res in enumerate(results, 1):
                formatted_results.append(to_metadata(res))
                if i == num_results:
                    break
            return formatted_results
