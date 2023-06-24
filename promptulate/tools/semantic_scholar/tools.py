from typing import Union, List, Dict

from pydantic import Field

from promptulate.tools.base import BaseTool
from promptulate.tools.semantic_scholar.api_wrapper import SemanticScholarAPIWrapper
from promptulate.utils.core_utils import listdict_to_string


class SemanticScholarQueryTool(BaseTool):
    name = "semantic-scholar-query"
    description = ""
    api_wrapper: SemanticScholarAPIWrapper = Field(
        default_factory=SemanticScholarAPIWrapper
    )

    def run(self, query: str, **kwargs) -> Union[str, List[Dict]]:
        result = self.api_wrapper.get_paper(query, **kwargs)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result, item_suffix="\n\n")


class SemanticScholarReferenceTool(BaseTool):
    name = "semantic-scholar-reference-tool"
    description = ""
    api_wrapper: SemanticScholarAPIWrapper = Field(
        default_factory=SemanticScholarAPIWrapper
    )

    def run(self, query: str, **kwargs) -> Union[str, List[Dict]]:
        result = self.api_wrapper.get_references(query)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result, item_suffix="\n\n")


class SemanticScholarCitationTool(BaseTool):
    name = "semantic-scholar-citation-tool"
    description = ""
    api_wrapper: SemanticScholarAPIWrapper = Field(
        default_factory=SemanticScholarAPIWrapper
    )

    def run(self, query: str, **kwargs) -> Union[str, List[Dict]]:
        result = self.api_wrapper.get_citations(query)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result, item_suffix="\n\n")
