# Copyright (c) 2023 Zeeland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/prompt-me
# Contact Email: zeeland@foxmail.com

import os
import time
import requests
from typing import Optional, List

from prompt_me import utils
from prompt_me.config import Config
from prompt_me.preset_role import BaseRole

__all__ = ['ChatBot']

cache = utils.get_cache()
logger = utils.get_logger()
CFG = Config()


class ChatBot:
    def __init__(self, key: Optional[str] = None, enable_proxy: bool = True):
        if not key and "OPENAI_API_KEY" not in os.environ.keys():
            raise ValueError('OPENAI API key is not provided')
        self.key = key if key else os.getenv('OPENAI_API_KEY')

        CFG.set_enable_proxy(enable_proxy)

    def ask(self, msg: str, conversation_id: Optional[str] = None) -> Optional[tuple]:
        """
        ask him a question, return his answer and a conversation_id. You can
        continue your session when you input your conversation_id.

        Args:
            msg: the message you can to ask
            conversation_id: conversation id

        Returns:
            a tuple like ->(his_answer: str, conversation_id: str)
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

        response = requests.post(url=CFG.get_request_url(), headers=headers, json=body)
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
        Get a complete conversation messages.

        Args:
            msg:
            conversation_id:

        Returns:
            conversation_id, messages

        Examples:
             A message is as follows:
        ---------------------------------------------------------------
        [
            {"preset_role": "system", "content": "You are a helpful assistant."},
            {"preset_role": "user", "content": "Hello, Who are you?"}
            {"preset_role": "assistant", "content": "I am AI."}
        ]
        ---------------------------------------------------------------
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

        Args:
            conversation_id:

        Returns:
            conversation_id
        """
        if conversation_id and conversation_id in cache:
            return conversation_id
        return str(time.time())

    def get_history(self, conversation_id: str) -> Optional[List[dict]]:
        """
        get conversation from cache

        Returns:
            conversation
        """
        if conversation_id in cache:
            return cache[conversation_id]
        return None

    def output(self, conversation_id: str, output_type: str = 'text', file_path: str = "output.md") -> Optional[str]:
        """
        Export conversation to markdown

        Args:
            conversation_id: conversation to export
            output_type: text or file, default is text
            file_path:  output file path

        Returns:
            conversation in markdown
        """
        conversation = self.get_history(conversation_id)
        if conversation is None:
            return None

        ret = "# Chat record\n"
        for message in conversation:
            role = message.get('preset_role')
            content = message.get('content').replace('"', '\\"')
            if role == 'assistant':
                ret += f"## Bot said\n\n{content}\n\n"
            else:
                ret += f"## You said\n\n{content}\n\n"
        if output_type == 'text':
            return ret
        elif output_type == 'file':
            with open(file_path, 'w') as f:
                f.write(ret)
        else:
            raise ValueError("Invalid output destination specified. Please choose either 'text' or 'file'.")
        return ret

    def _append_message_to_cache(self, msg: str, role: str, conversation_id: str) -> List[dict]:
        messages: List[dict] = cache[conversation_id]
        if role in ['user', 'assistant']:
            messages.append({"preset_role": role, "content": msg})
            cache[conversation_id] = messages
        return messages
