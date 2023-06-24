from unittest import TestCase

from promptulate.tools.arxiv.api_wrapper import ArxivAPIWrapper
from promptulate.tools.arxiv.tools import (
    ArxivSummaryTool,
    ArxivQueryTool,
    ArxivReferenceTool,
)
from promptulate.utils.logger import get_logger, enable_log

enable_log()
logger = get_logger()


class TestArxivApiWrapper(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arxiv_api_wrapper = ArxivAPIWrapper()

    def test_query_by_keyword(self):
        results = self.arxiv_api_wrapper.query("LLM")
        logger.info(results)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), self.arxiv_api_wrapper.max_num_of_result)

    def test_query_by_arxiv_id(self):
        results = self.arxiv_api_wrapper.query(id_list=["1605.08386v1"])
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)

    def test_query_by_filter(self):
        keys = ["entry_id", "title", "authors", "summary"]
        result = self.arxiv_api_wrapper.query(
            "Tree of Thoughts: Deliberate Problem Solving with Large Language Models",
            specified_fields=keys,
        )
        logger.info(result)
        for item in result:
            print(item)
        self.assertIsNotNone(result[0]["title"])
        self.assertIsNotNone(result[0]["entry_id"])
        self.assertIsNotNone(result[0]["authors"])
        self.assertIsNotNone(result[0]["summary"])

    # def test_arxiv_api_wrapper_download_dpf(self):
    #     result = self.arxiv_api_wrapper.download_pdf(["1605.08386v1"])
    #     self.assertIsNotNone(result)


class TestArxivTools(TestCase):
    def test_arxiv_query_tool(self):
        tool = ArxivQueryTool()
        ret = tool.run("LLM")
        logger.info(ret)
        self.assertIsNotNone(ret)
        self.assertIsInstance(ret, str)

    def test_arxiv_query_tool_by_specified_fields(self):
        tool = ArxivQueryTool()
        ret = tool.run("LLM", specified_fields=["entry_id", "title"])
        logger.info(ret)
        self.assertIsNotNone(ret)
        self.assertTrue("entry_id" in ret)
        self.assertTrue("title" in ret)
        self.assertTrue("summary" not in ret)
        self.assertTrue("authors" not in ret)

    def test_arxiv_reference_tool(self):
        tool = ArxivReferenceTool()
        prompt = """
        该论文探讨了Codex语言模型的Text-to-SQL能力，并对其在Spider基准测试中的表现进行了实证评估。研究发现，即使没有任何fine-tuning，Codex也是Spider基准测试中的强基准。同时，该研究还分析了Codex在这种情况下的失效模式。此外，该论文还在GeoQuery和Scholar基准测试中进行了实验，表明一小部分in-domain样例可以在不进行fine-tuning的情况下提高Codex的性能，并使其胜过在少量样例上进行finetune的最先进模型。
        该论文的一个关键见解是，语言模型的表现在很大程度上依赖于领域的样本数据。但是，该研究表明，在语言模型具备一定的常识知识和推理能力的情况下，提供一些领域内例子可以显著地提高它的性能。这意味着，我们并不总是需要进行大量的finetuning操作就能使模型在某些针对性任务上获得良好的表现。而且，在某些情况下，提供数据的方式也许比finetuning更为高效。
        该论文的经验教训是，我们需要在不同的语言模型和关键任务上进行评估，以便更好地了解它们的优缺点。此外，在一些应用场景中，我们可以通过提供一些in-domain例子来改进模型。
        """
        ret = tool.run(prompt)
        self.assertTrue("[1]" in ret)

    def test_arxiv_summary_tool(self):
        tool = ArxivSummaryTool()
        ret = tool.run("Large Language Models are Zero-Shot Reasoners")
        logger.info(f"[result] {ret}")
        self.assertIsNotNone(ret)

    def test_arxiv_summary_tool_by_arxiv_id(self):
        tool = ArxivSummaryTool()
        ret = tool.run("2205.11916v4")
        logger.info(f"[result] {ret}")
        self.assertIsNotNone(ret)
