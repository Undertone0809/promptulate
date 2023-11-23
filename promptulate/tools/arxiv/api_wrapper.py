from typing import Dict, List, Optional, Union

import arxiv
from pydantic import BaseModel, root_validator


class ArxivQuerySet:
    def __init__(self, search: arxiv.Search, keys: Optional[List[str]] = None):
        self.search: arxiv.Search = search
        self._data: List[Dict] = []

        for result in search.results():
            if keys:
                filtered_result_dict = {
                    k: result.__dict__[k] for k in keys if k in result.__dict__
                }
                self._data.append(filtered_result_dict)
            else:
                self._data.append(result.__dict__)

    def __str__(self):
        result: str = ""
        for item in self._data:
            result += f"{item.__dict__}\n"
        return result

    def titles(self) -> List[str]:
        titles: List[str] = []
        for item in self.search.results():
            titles.append(item.title)
        return titles

    def all(self) -> List[Dict]:
        return self._data

    def first(self) -> Optional[Dict]:
        if len(self._data) == 0:
            return None
        return self._data[0]

    @classmethod
    def from_filter_result(cls, search: arxiv.Search, *args):
        """generate a filter key queryset"""
        return cls(search, list(args))


class ArxivAPIWrapper(BaseModel):
    """https://github.com/lukasschwab/arxiv.py"""

    max_num_of_result: int = 5
    sort_by = arxiv.SortCriterion.Relevance

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    @root_validator(skip_on_failure=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that python package exists in environment."""
        try:
            import arxiv  # noqa
        except ImportError:
            raise ValueError(
                "Could not import arxiv python package. "
                "Please install it with `pip install arxiv`."
            )
        return values

    def _query(
        self,
        keyword: Optional[str] = None,
        id_list: Union[List[str], str, None] = None,
        num_results: Optional[int] = None,
    ) -> arxiv.Search:
        """
        query arxiv paper by keyword or id_list
        Args:
            keyword: query keyword
            id_list: arxiv id, you can input multiple id or single
        Returns:
            arxiv search type data result
        """
        if not keyword:
            keyword = ""

        if not id_list:
            id_list = []

        if not num_results:
            num_results = self.max_num_of_result

        if isinstance(id_list, str):
            id_list = [id_list]

        search = arxiv.Search(
            query=keyword,
            id_list=id_list,
            max_results=num_results,
            sort_by=self.sort_by,
        )
        return search

    def query(
        self,
        keyword: Optional[str] = None,
        id_list: Union[List[str], str, None] = None,
        num_results: Optional[int] = None,
        **kwargs,
    ) -> List[Dict]:
        """
        Query arxiv paper by keyword or id_list. You can make ArxivQuerySet return the
        specified fields from arxiv query result.
        Args:
            num_results: max num of result. Return self.max_num_of_result if none
            keyword: query keyword
            id_list: arxiv id, you can input multiple id or single
            kwargs:
                specified_fields(Optional[List[str]]): filter specified field to return.
                For example, you can return the ["title", "summary"] fields from each
                arxiv query result.
        Returns:
            List[Dict] type result
        Examples:
            If you want to get paper title and summary, you can do as follows.

            >> arxiv_api_wrapper = ArxivAPIWrapper()
            >> result = arxiv_api_wrapper.query("LLM", specified_fields=["entry_id", "title", "summary"])

            All fields you can see in: https://github.com/lukasschwab/arxiv.py
            Common fields are: ["entry_id", "title", "authors", "summary", "published"]
        """  # noqa
        search = self._query(keyword, id_list, num_results)
        if "specified_fields" in kwargs:
            return ArxivQuerySet.from_filter_result(
                search, *kwargs["specified_fields"]
            ).all()
        if "from_callback" in kwargs and kwargs["from_callback"] == "arxiv-query":
            keys = ["entry_id", "title", "authors", "summary"]
            return ArxivQuerySet.from_filter_result(search, *keys).all()
        return ArxivQuerySet(search).all()

    def download_pdf(self, id_list: List[str]) -> str:
        paper = next(arxiv.Search(id_list=id_list).results())
        return paper.download_pdf()
