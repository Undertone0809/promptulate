from unittest import TestCase

from promptulate.llms.openai import ChatOpenAI, OpenAI
from promptulate.schema import MessageSet, UserMessage
from promptulate.utils.logger import logger


class TestOpenAI(TestCase):
    def test_call(self):
        llm = OpenAI()
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test [end]
        ```
        """
        result = llm(prompt)
        self.assertIsNotNone(result)
        self.assertTrue("[start] This is a test [end]")

    def test_call_with_stop(self):
        llm = OpenAI(temperature=0)
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test [end]
        ```
        """
        result = llm(prompt, stop=["[end]"])
        self.assertIsNotNone(result)
        self.assertTrue("This is a test" in result)

    def test_generate_prompt_by_retry(self):
        pass


class TestOpenAIChat(TestCase):
    def test_call(self):
        llm = ChatOpenAI()
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test [end]
        ```
        """
        result = llm(prompt)
        self.assertIsNotNone(result)
        self.assertTrue("[start] This is a test [end]")

    def test_call_with_stop(self):
        llm = ChatOpenAI(temperature=0)
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test [end]
        ```
        """
        result = llm(prompt, stop=["test"])
        self.assertTrue("test [end]" not in result)
        self.assertIsNotNone(result)

    def test_generate_prompt(self):
        llm = ChatOpenAI()
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test [end]
        ```
        """
        user_message = UserMessage(content=prompt)
        result = llm.predict(MessageSet(messages=[user_message]))
        self.assertIsNotNone(result)

    def test_generate_prompt_by_retry(self):
        pass
