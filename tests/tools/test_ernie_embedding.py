from unittest import TestCase

from promptulate import enable_log
from promptulate.embeddings import ErnieEmbeddings

enable_log()


class TestErnieEmbedding(TestCase):
    def test_run(self):
        embedding = ErnieEmbeddings()
        result = embedding.embed_query("鸡你太美")
        result2 = embedding.embed_documents(["你好", "你很好"])
        print(result)
        print(result2)
