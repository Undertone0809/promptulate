from unittest import TestCase

from promptulate import Conversation, enable_log
from promptulate.llms import ErnieBot

enable_log()


class TestErnieBotAdapt(TestCase):
    def test_run(self):
        llm = ErnieBot()
        conversation = Conversation(llm=llm, role="linux-terminal")
        while True:
            prompt = str(input("[User] "))
            ret = conversation.predict(prompt)
            print(f"[output] {ret}")
