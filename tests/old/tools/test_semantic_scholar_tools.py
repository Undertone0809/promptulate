from unittest import TestCase

from promptulate.tools.semantic_scholar.api_wrapper import SemanticScholarAPIWrapper
from promptulate.tools.semantic_scholar.tools import (
    SemanticScholarCitationTool,
    SemanticScholarQueryTool,
    SemanticScholarReferenceTool,
)


class TestSemanticScholarApiWrapper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_wrapper = SemanticScholarAPIWrapper()

    def test_query_by_keyword(self):
        papers = self.api_wrapper.get_paper("Attention is all you need")
        self.assertIsNotNone(papers[0]["id"])
        self.assertIsNotNone(papers[0]["authorsYear"])
        self.assertIsNotNone(papers[0]["title"])
        self.assertIsNotNone(papers[0]["url"])

    def test_query_by_specified_fields(self):
        fields = ["title", "url", "abstract", "referenceCount"]
        references = self.api_wrapper.get_paper(
            "Attention is all you need", specified_fields=fields
        )
        self.assertIsNotNone(references[0]["id"])
        self.assertIsNotNone(references[0]["title"])
        self.assertIsNotNone(references[0]["url"])
        self.assertIsNotNone(references[0]["abstract"])
        self.assertIsNotNone(references[0]["referenceCount"])

    def test_get_references(self):
        references = self.api_wrapper.get_references("Attention is all you need")
        self.assertIsNotNone(references[0])
        self.assertIsNotNone(references[0]["id"])
        self.assertIsNotNone(references[0]["title"])
        self.assertIsNotNone(references[0]["url"])

    def test_get_citations(self):
        citations = self.api_wrapper.get_citations("Attention is all you need")
        self.assertIsNotNone(citations[0])
        self.assertIsNotNone(citations[0]["id"])
        self.assertIsNotNone(citations[0]["title"])
        self.assertIsNotNone(citations[0]["url"])


class TestSemanticScholarQueryTool(TestCase):
    def test_run(self):
        tool = SemanticScholarQueryTool()
        result = tool.run("attention is all you need")
        self.assertTrue("id" in result)
        self.assertTrue("authorsYear" in result)
        self.assertTrue("title" in result)
        self.assertTrue("url" in result)

    def test_run_return_specified_fields(self):
        tool = SemanticScholarQueryTool()
        fields = ["title", "url", "abstract", "referenceCount"]
        result = tool.run("attention is all you need", specified_fields=fields)
        self.assertTrue("id" in result)
        self.assertTrue("title" in result)
        self.assertTrue("url" in result)
        self.assertTrue("abstract" in result)
        self.assertTrue("referenceCount" in result)


class TestSemanticScholarReferenceTool(TestCase):
    def test_run(self):
        tool = SemanticScholarReferenceTool()
        result = tool.run("attention is all you need")
        self.assertTrue("id" in result)
        self.assertTrue("title" in result)
        self.assertTrue("url" in result)

    def test_run_return_listdict(self):
        tool = SemanticScholarReferenceTool()
        result = tool.run("attention is all you need", return_type="original")
        self.assertIsNotNone(result[0])
        self.assertIsNotNone(result[0]["id"])
        self.assertIsNotNone(result[0]["title"])
        self.assertIsNotNone(result[0]["url"])

    def test_run_with_max_result(self):
        tool = SemanticScholarReferenceTool()
        result = tool.run(
            "attention is all you need", max_result=5, return_type="original"
        )
        self.assertEqual(len(result), 5)
        self.assertIsNotNone(result[0])
        self.assertIsNotNone(result[0]["id"])
        self.assertIsNotNone(result[0]["title"])
        self.assertIsNotNone(result[0]["url"])


class TestSemanticScholarCitationTool(TestCase):
    def test_run(self):
        tool = SemanticScholarCitationTool()
        result = tool.run("attention is all you need")
        self.assertTrue("id" in result)
        self.assertTrue("title" in result)
        self.assertTrue("url" in result)

    def test_run_return_listdict(self):
        tool = SemanticScholarCitationTool()
        result = tool.run("attention is all you need", return_type="original")
        self.assertIsNotNone(result[0])
        self.assertIsNotNone(result[0]["id"])
        self.assertIsNotNone(result[0]["title"])
        self.assertIsNotNone(result[0]["url"])
