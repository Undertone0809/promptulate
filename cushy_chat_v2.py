# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 23:02
# @Author  : Zeeland
# @File    : cushy_chat.py
# @Software: PyCharm
# @Link    : https://platform.openai.com/docs/api-reference/chat/create

import time
import logging
import requests
from typing import Optional, List
from cushy_storage import CushyDict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
URL = 'https://chatgpt-api.shn.hk/v1/'  # FREE API
cache = CushyDict("./cache")


# 初始化一个类
class ChatBot:
    def __init__(self, key):
        self.key = key

    def ask(self, msg: str, conversation_id: Optional[str] = None) -> Optional[tuple]:
        """
        ask him a question, return his answer and a conversation_id. You can
        continue your session when you input your conversation_id.
        :param msg: the message you can to ask
        :param conversation_id: conversation_id to keep session
        :return: a tuple like ->(his_answer: str, conversation_id: str)
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}"
        }

        conversation_id, messages = self._get_message_from_cache(msg, conversation_id)
        cache[conversation_id] = messages
        body = {
            "model": "gpt-3.5-turbo",
            "messages": messages
        }
        logger.debug(body)

        response = requests.post(url=URL, headers=headers, json=body)
        if response.status_code == 200:
            ret_data = response.json()
            logger.debug(ret_data)
            ret_msg = ret_data['choices'][0]['message']['content']
            logger.debug(ret_msg)
            self._append_message_to_cache(ret_msg, 'assistant', conversation_id)
            return ret_msg, conversation_id

        logger.error("Failed to get data")
        return None

    def _get_message_from_cache(self, msg: str, conversation_id: Optional[str] = None) -> tuple:
        """
        get a complete messages. A message is as follows:
        ---------------------------------------------------------------
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, Who are you?"}
            {"role": "assistant", "content": "I am AI."}
        ]
        ---------------------------------------------------------------
        :param conversation_id:
        :return: conversation_id, messages
        """
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": msg}
        ]
        if self._is_old_conversation(conversation_id):
            messages = self._append_message_to_cache(msg, 'user', conversation_id)
            return conversation_id, messages
        return self._get_conversation_id(), messages

    def _is_old_conversation(self, conversation_id: Optional[str]) -> bool:
        return conversation_id == self._get_conversation_id(conversation_id)

    def _get_conversation_id(self, conversation_id: Optional[str] = None) -> str:
        """
        This function has two functions. Generating a new conversation_id if it
        doesn't exist, otherwise the same conversation_id as the input is returned.
        :return: conversation_id
        """
        if conversation_id and conversation_id in cache:
            return conversation_id
        return str(time.time())

    def _append_message_to_cache(self, msg: str, role: str, conversation_id: str) -> List[dict]:
        messages: List[dict] = cache[conversation_id]
        if role in ['user', 'assistant']:
            messages.append({"role": role, "content": msg})
            cache[conversation_id] = messages
        return messages


def main():
    print("A Simple ChatBot built by ChatGPT API")
    conversation_id = None
    while True:
        prompt = str(input("[User] "))
        bot = ChatBot(key='key')
        ret, conversation_id = bot.ask(prompt, conversation_id)
        print(ret, conversation_id)


if __name__ == '__main__':
    main()
