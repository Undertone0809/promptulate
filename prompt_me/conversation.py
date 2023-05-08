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

import time
import requests
from typing import Optional, List

from prompt_me import utils
from prompt_me.config import Config
from prompt_me.preset_role import BaseRole, DefaultRole

__all__ = ['Conversation']

cache = utils.get_cache()
logger = utils.get_logger()
CFG = Config()


class Conversation:
    """Create a conversation. You can set a default preset_role for conversations."""

    def __init__(self, role: BaseRole = DefaultRole(), enable_proxy: bool = True):
        CFG.set_enable_proxy(enable_proxy)
        logger.debug(f"[OPENAI_API_KEY] {CFG.openai_api_key}")

        self.role: BaseRole = role
        self.conversation_id = None

    def predict(self, msg: str) -> Optional[str]:
        """
        ask him a question, return his answer and a conversation_id. You can
        continue your session when you input your conversation_id.

        Args:
            msg: the message you can ask

        Returns:
            a tuple like ->(his_answer: str, conversation_id: str)
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CFG.openai_api_key}"
        }

        messages = self._get_message_from_cache(msg)
        cache[self.conversation_id] = messages
        body = {
            "model": "gpt-3.5-turbo",
            "messages": messages
        }
        logger.debug(body)

        response = requests.post(url=CFG.get_request_url(), headers=headers, json=body, stream=True)
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=None):
                print(chunk)
            ret_data = response.json()
            logger.debug(ret_data)
            ret_msg = ret_data['choices'][0]['message']['content']
            logger.debug(ret_msg)
            self._append_message_to_cache(ret_msg, 'assistant')
            return ret_msg

        logger.error("Failed to get data. Please check your network or api key.")
        return None

    def _get_message_from_cache(self, msg: str) -> List[dict]:
        """
        Get a complete conversation messages.

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
            {"role": "system", "content": self.role.description},
            {"role": "user", "content": msg}
        ]

        if self._is_new_conversation():
            self._generate_conversation_id()
            return messages
        messages = self._append_message_to_cache(msg, 'user')
        return messages

    def _is_new_conversation(self) -> bool:
        return self.conversation_id is None

    def _generate_conversation_id(self) -> None:
        """Generating a new conversation_id if it doesn't exist."""
        self.conversation_id = str(int(time.time()))

    def get_history(self) -> Optional[List[dict]]:
        """
        get conversation from cache

        Returns:
            conversation
        """
        if self.conversation_id in cache:
            return cache[self.conversation_id]
        return None

    def output(self, output_type: str = 'text', file_path: str = "output.md") -> Optional[str]:
        """
        Export conversation to markdown

        Args:
            output_type: text or file, default is text
            file_path:  output file path

        Returns:
            conversation in markdown
        """
        conversation = self.get_history()
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

    def _append_message_to_cache(self, msg: str, role: str) -> List[dict]:
        messages: List[dict] = cache[self.conversation_id]
        if role in ['user', 'assistant']:
            messages.append({"role": role, "content": msg})
            cache[self.conversation_id] = messages
        return messages
