import json
from typing import List, Optional, Dict

import requests
from pydantic import BaseModel

from promptulate.tips import NetWorkError
from promptulate.utils.logger import get_logger

logger = get_logger()


class SemanticScholarAPIWrapper(BaseModel):
    """https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/"""

    BASE_API_URL: str = "https://api.semanticscholar.org/graph/v1"
    BASE_OFFICIAL_URL: str = "https://www.semanticscholar.org"
    current_result: Optional[List[Dict]] = None
    paper_query_params: Dict[str, str] = {"fields": "title,url,abstract"}

    def get_paper(self, query: str, **kwargs) -> List[Dict]:
        """This method can obtain a list of relevant papers based on your query.

        Args:
            query: keyword to search paper
            **kwargs:
                specified_fields(Optional[List[str]]): filter specified field to return.
                For example, you can return the ["title", "url", "abstract"] fields from each arxiv query result.
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
            paper_ids = list(map(lambda p: p["id"], self.current_result))
            fields: List[str] = kwargs["specified_fields"]
            params: Dict[str, str] = {"fields": ",".join(fields)}

            r = requests.post(
                f"{self.BASE_API_URL}/paper/batch",
                params=params,
                json={"ids": paper_ids},
            )
            if response.status_code != 200:
                raise NetWorkError("")

            detail_result = r.json()
            for original in self.current_result:
                for detail_item in detail_result:
                    if detail_item["paperId"] == original["id"]:
                        original.update(detail_item)
            return

        query = "%20".join(query.split(" "))
        url = f"{self.BASE_API_URL}/paper/autocomplete?query={query}"
        response = requests.get(url)
        if response.status_code == 200:
            self.current_result = response.json()["matches"]

            if len(self.current_result) == 0:
                return []

            for item in self.current_result:
                item["url"] = self._get_url(item["id"])
                if "specified_fields" in kwargs:
                    get_detail()
            logger.debug(
                f"[promptulate semantic scholar result] {json.dumps(self.current_result)}"
            )
            return self.current_result
        raise NetWorkError("semantic scholar query")

    def _get_url(self, id: str) -> str:
        return f"{self.BASE_OFFICIAL_URL}/paper/{id}"

    def get_references(self, query: str) -> List[Dict]:
        """Used to get references of specified paper.

        Args:
            query: the keyword you want to query

        Returns:
            Return List[Dict] data, the default detail fields is as follows.
            - id (str): semantic id
            - authorsYear (str): author and publication year
            - title (str): paper title
            - url (str): paper semantic scholar url
        """
        if len(self.get_paper(query)) == 0:
            return []

        paper_id: str = self.get_paper(query)[0]["id"]
        url = f"{self.BASE_API_URL}/paper/{paper_id}/references"
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

            logger.debug(
                f"[promptulate semantic scholar result] {json.dumps(final_result)}"
            )
            return final_result
        raise NetWorkError("semantic scholar")
