from unittest import TestCase
from promptulate.schema import LLMPrompt, UserMessage
from promptulate.llms.openai import OpenAI
from promptulate.utils.logger import get_logger, enable_log

enable_log()
logger = get_logger()


class TestOpenAI(TestCase):
    def test_call(self):
        llm = OpenAI()
        result = llm("What is LLM")
        logger.info(result)
        self.assertIsNotNone(result)

    def test_generate_prompt(self):
        llm = OpenAI()
        user_message = UserMessage(content="What is LLM")
        result = llm.generate_prompt(LLMPrompt(messages=[user_message]))
        logger.info(result)
        self.assertIsNotNone(result)

    def test_generate_prompt_by_retry(self):
        pass
