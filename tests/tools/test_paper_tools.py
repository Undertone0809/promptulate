# from unittest import TestCase

# from promptulate.tools.paper.tools import PaperSummaryTool
# from promptulate.utils.logger import  get_logger

# logger = get_logger()


# class TestPaperSummaryTool(TestCase):
#     def test_run(self):
#         tool = PaperSummaryTool()
#         result = tool.run("attention is all you need")
#         logger.info(f"[result] {result}")
#         self.assertIsNotNone(result)
#         self.assertTrue("[1]" in result)
#         self.assertTrue("关键见解" in result)
#         self.assertTrue("经验教训" in result)
#         self.assertTrue("相关建议" in result)

#     def test_by_arxiv_id(self):
#         tool = PaperSummaryTool()
#         result = tool.run("2205.11916v4")
#         logger.info(f"[result] {result}")
#         self.assertIsNotNone(result)
#         self.assertTrue("[1]" in result)
#         self.assertTrue("关键见解" in result)
#         self.assertTrue("经验教训" in result)
#         self.assertTrue("相关建议" in result)
