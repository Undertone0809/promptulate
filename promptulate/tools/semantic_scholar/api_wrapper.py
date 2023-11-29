import json
import time
from typing import Dict, List, Optional

import requests
from pydantic import BaseModel

from promptulate.error import NetWorkError
from promptulate.utils.logger import logger


class SemanticScholarAPIWrapper(BaseModel):
    """https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/"""

    BASE_API_URL: str = "https://api.semanticscholar.org/graph/v1"
    BASE_OFFICIAL_URL: str = "https://www.semanticscholar.org"
    max_result: int = 10
    current_result: Optional[List[Dict]] = None
    paper_query_params: Dict[str, str] = {"fields": "title,url,abstract"}

    def _get_string_fields(self) -> str:
        return f"&fields={self.paper_query_params['fields']}&"

    def get_paper(
        self, query: str, max_result: Optional[int] = None, **kwargs
    ) -> List[Dict]:
        """This method can obtain a list of relevant papers based on your query.

        Args:
            max_result: num of max result
            query: the papers you want to query
            **kwargs:
                specified_fields(Optional[List[str]]): filter specified field to return.
                For example, you can return the ["title", "url", "abstract"] fields from
                each arxiv query result.
                You can see the detail fields as follows:
                https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers

        Returns:
            Return List[Dict] data, the default detail fields is as follows.
            - id (str): semantic id
            - authorsYear (str): author and publication year
            - title (str): paper title
            - url (str): paper semantic scholar url
            If you want to get more detail fields, please use `specified_fields`
        """

        def get_detail():
            """
            Get more paper attributions for specified_fields.
            ref: https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers
            """
            paper_ids = list(map(lambda p: p["id"], self.current_result))
            fields: List[str] = kwargs["specified_fields"]
            params: Dict[str, str] = {"fields": ",".join(fields)}

            resp = requests.post(
                f"{self.BASE_API_URL}/paper/batch",
                params=params,
                json={"ids": paper_ids},
            )
            if response.status_code != 200:
                raise NetWorkError("SemanticScholarAPIWrapper.get_paper.get_detail")

            detail_result = resp.json()
            if isinstance(detail_result, dict):
                raise NetWorkError(
                    "SemanticScholarAPIWrapper.get_paper.get_detail",
                    reason=detail_result["message"],
                )

            detail_result = resp.json()

            time.sleep(0.1)

            for original in self.current_result:
                for detail_item in detail_result:
                    if detail_item["paperId"] == original["id"]:
                        original.update(detail_item)
            return

        if not max_result:
            max_result = self.max_result

        query = "%20".join(query.split(" "))
        url = f"{self.BASE_API_URL}/paper/autocomplete?query={query}&limit={max_result}"
        response = requests.get(url)
        if response.status_code == 200:
            self.current_result = response.json()["matches"]

            if len(self.current_result) == 0:
                logger.debug("[pne] semantic scholar return none")
                return []

            for item in self.current_result:
                item["url"] = self._get_url(item["id"])

            if "specified_fields" in kwargs:
                get_detail()
            logger.debug(
                f"[pne] semantic scholar result {json.dumps(self.current_result)}"
            )
            return self.current_result
        raise NetWorkError("semantic scholar query")

    def _get_url(self, id: str) -> str:
        """Get paper url from paper id."""
        return f"{self.BASE_OFFICIAL_URL}/paper/{id}"

    def get_references(self, query: str, max_result: int = 500, **kwargs) -> List[Dict]:
        """Used to get references of specified paper.

        Args:
            max_result: num of max result
            query: the paper you want to query

        Returns:
            Return List[Dict] data, the default detail fields is as follows.
            - id (str): semantic id
            - authorsYear (str): author and publication year
            - title (str): paper title
            - url (str): paper semantic scholar url
        """
        papers = self.get_paper(query)
        if len(papers) == 0:
            return []

        paper_id: str = papers[0]["id"]
        url = f"{self.BASE_API_URL}/paper/{paper_id}/references?offset=1&limit={max_result}"  # noqa
        response = requests.get(url)
        if response.status_code == 200:
            res_data = response.json()["data"]
            final_result: List[Dict] = []
            for i, item in enumerate(res_data):
                if not item["citedPaper"]["paperId"]:
                    continue

                item["citedPaper"]["url"] = self._get_url(item["citedPaper"]["paperId"])
                item["citedPaper"]["id"] = item["citedPaper"]["paperId"]
                del item["citedPaper"]["paperId"]
                final_result.append(item["citedPaper"])

            logger.debug(f"[pne semantic scholar result] {json.dumps(final_result)}")
            return final_result
        raise NetWorkError("semantic scholar")

    def get_citations(self, query: str, max_result: Optional[int] = None):
        """Used to get citation of specified paper.

        Args:
            max_result: num of max result
            query: the paper you want to query

        Returns:
            Return List[Dict] data, the default detail fields is as follows.
            - id (str): semantic id
            - abstract (str): paper abstract
            - title (str): paper title
            - url (str): paper semantic scholar url
        """
        papers = self.get_paper(query)
        if len(papers) == 0:
            return []
        if not max_result:
            max_result = self.max_result

        paper_id: str = papers[0]["id"]
        url = f"{self.BASE_API_URL}/paper/{paper_id}/citations?{self._get_string_fields()}offset=1&limit={max_result}"  # noqa

        response = requests.get(url)
        if response.status_code == 200:
            res_data = response.json()["data"]
            final_result: List[Dict] = []

            for i, item in enumerate(res_data):
                if not item["citingPaper"].get("paperId"):
                    continue

                item["citingPaper"]["url"] = self._get_url(
                    item["citingPaper"]["paperId"]
                )
                item["citingPaper"]["id"] = item["citingPaper"]["paperId"]
                del item["citingPaper"]["paperId"]
                final_result.append(item["citingPaper"])

            logger.debug(f"[pne semantic scholar result] {json.dumps(final_result)}")
            return final_result
        raise NetWorkError("semantic scholar")
