from unittest import TestCase

from promptulate.tools.duckduckgo.api_wrapper import DuckDuckGoSearchAPIWrapper
from promptulate.tools.duckduckgo.tools import DuckDuckGoTool, DuckDuckGoReferenceTool
from promptulate.utils.logger import get_logger, enable_log

enable_log()
logger = get_logger()


class TestDuckDuckGoSearchAPIWrapper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_wrapper = DuckDuckGoSearchAPIWrapper()

    def test_search_by_keyword(self):
        result = self.api_wrapper.query("LLM")
        self.assertIsNotNone(result)

    def test_get_formatted_result(self):
        results = self.api_wrapper.query_by_formatted_results("LLM", 5)
        for result in results:
            logger.info(result)
        self.assertIsNotNone(results[0]["snippet"])
        self.assertIsNotNone(results[0]["title"])
        self.assertIsNotNone(results[0]["link"])


class TestDuckDuckGoSearchTool(TestCase):
    def test_query(self):
        tool = DuckDuckGoTool()
        query = "请介绍一下promptulate框架"
        result = tool.run(query)
        logger.info(result)


class TestDuckDuckGoReferenceTool(TestCase):
    def test_query(self):
        tool = DuckDuckGoReferenceTool()
        result = tool.run("LLM", num_results=1)
        logger.info(result)
        self.assertTrue("snippet" in result)
        self.assertTrue("title" in result)
        self.assertTrue("link" in result)

    def test_query_by_json(self):
        tool = DuckDuckGoReferenceTool()
        results = tool.run("LLM", num_results=6, return_type="original")
        logger.info(results)
        self.assertIsNotNone(results[0]["snippet"])
        self.assertIsNotNone(results[0]["title"])
        self.assertIsNotNone(results[0]["link"])
        self.assertEqual(6, len(results))
