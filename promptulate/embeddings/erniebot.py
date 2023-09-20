import threading
from typing import Optional, Dict, List

import requests
from pydantic import BaseModel, root_validator

from promptulate.config import Config
from promptulate.embeddings.base import Embeddings
from promptulate.utils import get_logger

logger = get_logger()
CFG = Config()


class ErnieEmbeddings(BaseModel, Embeddings):
    """`Ernie Embeddings V1` embedding models."""

    access_token: Optional[str] = ""

    chunk_size: int = 16

    model_name = "ErnieBot-Embedding-V1"

    url: str = CFG.ernie_embedding_v1_url

    def _embedding(self, json: object) -> dict:
        resp = requests.post(
            url=self.url + "?access_token=" + self.access_token,
            headers={
                "Content-Type": "application/json",
            },
            json=json,
        )
        return resp.json()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs.

        Args:
            texts: The list of texts to embed

        Returns:
            List[List[float]]: List of embeddings, one for each text.
        """

        if not self.access_token:
            self.access_token = CFG.get_ernie_token()
        text_in_chunks = [
            texts[i : i + self.chunk_size]
            for i in range(0, len(texts), self.chunk_size)
        ]
        lst = []
        for chunk in text_in_chunks:
            resp = self._embedding({"input": [text for text in chunk]})
            if resp.get("error_code"):
                if resp.get("error_code") == 110:
                    self.access_token = CFG.get_ernie_token()
                    resp = self._embedding({"input": [text for text in chunk]})
                else:
                    raise ValueError(f"Error from Ernie: {resp}")
            lst.extend([i["embedding"] for i in resp["data"]])
        return lst

    def embed_query(self, text: str) -> List[float]:
        """Embed query text.

        Args:
            text: The text to embed.

        Returns:
            List[float]: Embeddings for the text.
        """

        if not self.access_token:
            self.access_token = CFG.get_ernie_token()
        resp = self._embedding({"input": [text]})
        if resp.get("error_code"):
            if resp.get("error_code") == 110:
                self.access_token = CFG.get_ernie_token()
                resp = self._embedding({"input": [text]})
            else:
                raise ValueError(f"Error from Ernie: {resp}")
        return resp["data"][0]["embedding"]
