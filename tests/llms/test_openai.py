from unittest import TestCase

from promptulate.llms.openai import OpenAI, ChatOpenAI
from promptulate.schema import LLMPrompt, UserMessage
from promptulate.utils.logger import get_logger, enable_log

enable_log()
logger = get_logger()


class TestOpenAI(TestCase):
    def test_call(self):
        llm = OpenAI()
        result = llm("什么是引力波？")
        self.assertIsNotNone(result)

    def test_call_with_stop(self):
        llm = OpenAI()
        result = llm("什么是引力波？")
        self.assertIsNotNone(result)

    def test_generate_prompt_by_retry(self):
        pass


class TestOpenAIChat(TestCase):
    def test_call(self):
        llm = ChatOpenAI()
        result = llm("大语言模型是什么？")
        logger.info(result)
        self.assertIsNotNone(result)

    def test_generate_prompt(self):
        llm = ChatOpenAI()
        user_message = UserMessage(content="What is LLM")
        result = llm.generate_prompt(LLMPrompt(messages=[user_message]))
        logger.info(result)
        self.assertIsNotNone(result)

    def test_generate_prompt_by_retry(self):
        pass
