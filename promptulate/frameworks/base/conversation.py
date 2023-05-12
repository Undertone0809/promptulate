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
# Project Link: https://github.com/Undertone0809/promptulate
# Contact Email: zeeland@foxmail.com

import time
import requests
from typing import Optional, List, Union

from promptulate import utils
from promptulate.config import Config
from promptulate.frameworks.mixins import SummarizerMixin
from promptulate.preset_roles import BaseRole, DefaultRole
from promptulate.llms import BaseLLM, OpenAI
from promptulate.frameworks.schema import BaseConversationFramework, BasePromptFramework
from promptulate.schema import (
    SystemMessage,
    UserMessage,
    BaseMessage,
    AssistantMessage,
    LocalCacheChatMessageHistory,
    BaseChatMessageHistory
)

CFG = Config()
logger = utils.get_logger()
cache = utils.get_cache()


def generate_conversation_id() -> str:
    """Generating a new conversation_id when a conversation initialize"""
    return str(int(time.time()))


class Conversation(BasePromptFramework, SummarizerMixin):
    role = DefaultRole()
    llm: BaseLLM = OpenAI()
    conversation_id: Optional[str] = None
    chat_message_history: BaseChatMessageHistory = LocalCacheChatMessageHistory()

    # todo 完成这里
    def predict(self, msg: str) -> Optional[str]:
        pass
    #     """
    #     ask a question, return his answer and a conversation_id. You can
    #     continue your session when you input your conversation_id.
    #
    #     Args:
    #         msg: the message you can ask
    #
    #     Returns:
    #         a tuple like ->(his_answer: str, conversation_id: str)
    #     """
    #
    #     self._get_message_from_cache()
    #     self.llm.generate_prompt()
    #     return None
    #
    # def _get_message_from_cache(self, msg: str) -> List[BaseMessage]:
    #     """
    #     Get a complete conversation messages.
    #
    #     Returns:
    #         conversation_id, messages
    #
    #     Examples:
    #          A message is as follows:
    #     ---------------------------------------------------------------
    #     [
    #         {"preset_roles": "system", "content": "You are a helpful assistant."},
    #         {"preset_roles": "user", "content": "Hello, Who are you?"}
    #         {"preset_roles": "assistant", "content": "I am AI."}
    #     ]
    #     ---------------------------------------------------------------
    #     """
    #
    #     self.chat_message_history.add_system_message(self.role.description)
    #     self.chat_message_history.add_user_message(msg)
    #
    #     # messages = [
    #     #     {"role": "system", "content": self.role.description},
    #     #     {"role": "user", "content": msg}
    #     # ]
    #
    #     if self._is_new_conversation():
    #         self.conversation_id = generate_conversation_id()
    #         return messages
    #     messages = self._append_message_to_cache(msg, 'user')
    #     return messages
    #
    # def _is_new_conversation(self) -> bool:
    #     logger.debug(f"[prompt_me] current conversation is [{self.conversation_id is None}] new conversation")
    #     return self.conversation_id is None

    # def get_history(self) -> Optional[List[dict]]:
    #     """
    #     get conversation from cache
    #
    #     Returns:
    #         conversation
    #     """
    #     if self.conversation_id in cache:
    #         return cache[self.conversation_id]
    #     return None
    #
    # def output(self, output_type: str = 'text', file_path: str = "output.md") -> Optional[str]:
    #     """
    #     Export conversation to markdown
    #
    #     Args:
    #         output_type: text or file, default is text
    #         file_path:  output file path
    #
    #     Returns:
    #         conversation in markdown
    #     """
    #     conversation = self.get_history()
    #     if conversation is None:
    #         return None
    #
    #     ret = "# Chat record\n"
    #     for message in conversation:
    #         role = message.get('preset_roles')
    #         content = message.get('content').replace('"', '\\"')
    #         if role == 'assistant':
    #             ret += f"## Bot said\n\n{content}\n\n"
    #         else:
    #             ret += f"## You said\n\n{content}\n\n"
    #     if output_type == 'text':
    #         return ret
    #     elif output_type == 'file':
    #         with open(file_path, 'w') as f:
    #             f.write(ret)
    #     else:
    #         raise ValueError("Invalid output destination specified. Please choose either 'text' or 'file'.")
    #     return ret

    # def _append_message_to_cache(self, msg: str, role: str) -> List[dict]:
    #     messages: List[dict] = cache[self.conversation_id]
    #     if role in ['user', 'assistant']:
    #         messages.append({"role": role, "content": msg})
    #         cache[self.conversation_id] = messages
    #     return messages


def main():
    conversation = Conversation()
    print(conversation.enable_proxy)


if __name__ == '__main__':
    main()
