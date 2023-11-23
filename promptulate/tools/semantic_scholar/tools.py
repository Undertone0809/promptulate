from typing import Dict, List, Union

from pydantic import Field

from promptulate.tools.base import BaseTool
from promptulate.tools.semantic_scholar.api_wrapper import SemanticScholarAPIWrapper
from promptulate.utils.core_utils import listdict_to_string


class SemanticScholarQueryTool(BaseTool):
    name: str = "semantic-scholar-query"
    description: str = (
        "A query tool around Semantic Scholar."
        "Useful for when you need to answer questions about Physics, Mathematics, "
        "Computer Science, Quantitative Biology, Quantitative Finance, Statistics, "
        "Electrical Engineering, and Economics "
        "from scientific articles on semantic scholar."
        "Input should be a search query."
    )
    api_wrapper: SemanticScholarAPIWrapper = Field(
        default_factory=SemanticScholarAPIWrapper
    )

    def _run(self, query: str, **kwargs) -> Union[str, List[Dict]]:
        """A semantic scholar paper query tool and return relevant paper query
        result."""
        result = self.api_wrapper.get_paper(query, **kwargs)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result, item_suffix="\n\n")


class SemanticScholarReferenceTool(BaseTool):
    name: str = "semantic-scholar-reference-tool"
    description: str = ""
    api_wrapper: SemanticScholarAPIWrapper = Field(
        default_factory=SemanticScholarAPIWrapper
    )

    def _run(self, query: str, **kwargs) -> Union[str, List[Dict]]:
        result = self.api_wrapper.get_references(query, **kwargs)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result, item_suffix="\n\n")


class SemanticScholarCitationTool(BaseTool):
    name: str = "semantic-scholar-citation-tool"
    description: str = ""
    api_wrapper: SemanticScholarAPIWrapper = Field(
        default_factory=SemanticScholarAPIWrapper
    )

    def _run(self, query: str, **kwargs) -> Union[str, List[Dict]]:
        result = self.api_wrapper.get_citations(query)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result, item_suffix="\n\n")
