from unittest import TestCase

from promptulate import Conversation, enable_log
from promptulate.llms import ErnieBot

enable_log()


class TestErnieBotAdapt(TestCase):
    def test_run(self):
        llm = ErnieBot(temperature=0.1)
        conversation = Conversation(llm=llm)
        while True:
            prompt = str(input("[User] "))
            ret = conversation.run(prompt)
            print(f"[output] {ret}")
