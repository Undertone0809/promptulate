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

from pydantic import BaseModel
from typing import List, Optional

from promptulate.llms.base import BaseLLM
from promptulate.memory.base import BaseChatMemory
from promptulate.frameworks.prompt import SUMMARY_CONTENT_PROMPT_ZH, SUMMARY_TOPIC_PROMPT_ZH
from promptulate.schema import (
    LLMPrompt,
    UserMessage,
    BaseMessage,
    AssistantMessage,
    ChatMessageHistory
)


class BaseMixin(BaseModel):
    llm: BaseLLM
    conversation_id: Optional[str]
    memory: BaseChatMemory

    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    def embed_message(self, cur_message: BaseMessage, message_history: ChatMessageHistory) -> None:
        message_history.messages.append(cur_message)
        self.memory.save_conversation_to_memory(message_history)


class SummarizerMixin(BaseMixin):
    """message summary capability provider"""

    def summary_content(self, enable_embed_message: bool = False, summary_prompt: str = SUMMARY_CONTENT_PROMPT_ZH):
        message_history = self.memory.load_conversation_from_memory(self.conversation_id)
        message_history.messages.append(UserMessage(content=summary_prompt))
        assistant_answer: AssistantMessage = self.llm.generate_prompt(LLMPrompt(messages=message_history.messages))
        if enable_embed_message:
            self.embed_message(assistant_answer, message_history)
        return assistant_answer.content

    def summary_topic(self, enable_embed_message: bool = False, summary_topic_prompt: str = SUMMARY_TOPIC_PROMPT_ZH):
        message_history = self.memory.load_conversation_from_memory(self.conversation_id)
        message_history.messages.append(
            UserMessage(content=summary_topic_prompt))
        assistant_answer: AssistantMessage = self.llm.generate_prompt(LLMPrompt(messages=message_history.messages))
        if enable_embed_message:
            self.embed_message(assistant_answer, message_history)
        return assistant_answer.content


class TranslatorMixin(BaseMixin):
    """let the llm answer question in the specified language"""

    def predict_by_translate(self, prompt: str, country: str, enable_embed_message: bool = False):
        """
        predict by specified language

        Args:
            enable_embed_message: Whether to save this session in the history session
            prompt: you prompt
            country: which country's language you want to export

        Returns:
            the country official language you choose
        """
        message_history = self.memory.load_conversation_from_memory(self.conversation_id)
        message_history.messages.append(
            UserMessage(content=f"{prompt}. Please answer question using {country} official language. "))
        assistant_answer: AssistantMessage = self.llm.generate_prompt(LLMPrompt(messages=message_history.messages))
        if enable_embed_message:
            self.embed_message(assistant_answer, message_history)
        return assistant_answer.content


class DeriveHistoryMessageMixin(BaseMixin):
    """provide history message output as markdown"""

    def get_history(self) -> List[dict]:
        """get history conversation from memory"""
        return self.memory.load_conversation_from_memory(self.conversation_id).listdict_message

    def export_message_to_markdown(self, output_type: str = 'text', file_path: str = "output.md") -> Optional[str]:
        """
        convert message to the string type or file type markdown

        Args:
            output_type: text or file. default is text
            file_path: output file path

        Returns:
            string type conversation in markdown format
        """
        message_history: List[dict] = self.get_history()

        ret = "# Chat record\n"
        for message in message_history:
            role = message.get('preset_roles')
            content = message.get('content').replace('"', '\\"')
            if role == 'assistant':
                ret += f"## Bot said\n\n{content}\n\n"
            else:
                ret += f"## You said\n\n{content}\n\n"
        if output_type == 'text':
            return ret
        elif output_type == 'file':
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(ret)
        else:
            raise ValueError("Invalid output destination specified. Please choose either 'text' or 'file'.")
        return ret


class StorageHistoryMessageMixin(BaseModel):
    pass
