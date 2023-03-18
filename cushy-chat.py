# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 23:02
# @Author  : Zeeland
# @File    : cushy-chat.py
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
API_KEY = "YOUR KEY HERE" # YOUR KEY
cache = CushyDict("./cache")


def get_answer(msg: str, conversation_id: Optional[str] = None) -> Optional[tuple]:
    """
    ask him a question, return his answer and a conversation_id. You can
    continue your session when you input your conversation_id.
    :param msg: the message you can to ask
    :param conversation_id: conversation_id to keep session
    :return: a tuple like ->(his_answer: str, conversation_id: str)
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    conversation_id, messages = _get_message_to_cache(msg, conversation_id)
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
        _append_message_to_cache(ret_msg, 'assistant', conversation_id)
        return ret_msg, conversation_id

    logger.error("Failed to get data")
    return None


def _get_message_to_cache(msg: str, conversation_id: Optional[str] = None) -> tuple:
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
    if _is_old_conversation(conversation_id):
        messages = _append_message_to_cache(msg, 'user', conversation_id)
        return conversation_id, messages
    return _get_conversation_id(), messages


def _is_old_conversation(conversation_id: Optional[str]) -> bool:
    return conversation_id == _get_conversation_id(conversation_id)


def _get_conversation_id(conversation_id: Optional[str] = None) -> str:
    """
    This function has two functions. Generating a new conversation_id if it
    doesn't exist, otherwise the same conversation_id as the input is returned.
    :return: conversation_id
    """
    if conversation_id and conversation_id in cache:
        return conversation_id
    return str(time.time())


def _append_message_to_cache(msg: str, role: str, conversation_id: str) -> List[dict]:
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
        ret, conversation_id = get_answer(prompt, conversation_id=conversation_id)
        print(f"[ChatBot] {ret}")


if __name__ == '__main__':
    main()
