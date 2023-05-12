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

import requests
from abc import ABC, abstractmethod
from pydantic import BaseModel, root_validator
from typing import List, Optional, Union, Any

from promptulate.utils import get_logger
from promptulate.config import Config
from promptulate.schema import (
    LLMPrompt,
    BaseMessage,
    UserMessage,
    SystemMessage,
    AssistantMessage,
    BaseChatMessageHistory,
    LocalCacheChatMessageHistory,
)

CFG = Config()
logger = get_logger()


class BaseLLM(BaseModel):
    @abstractmethod
    def generate_prompt(self, prompts: LLMPrompt) -> AssistantMessage:
        """llm generate prompt"""

    @abstractmethod
    def _parse_prompt(self, prompts: LLMPrompt) -> Any:
        """parse prompt"""

    @abstractmethod
    def __call__(self, prompt, *args, **kwargs):
        """input string prompt return answer"""


class OpenAI(BaseLLM):
    """https://platform.openai.com/docs/api-reference/chat/create"""

    model: str = "gpt-3.5-turbo"
    """Model name to use."""
    temperature: float = 1.0
    """What sampling temperature to use."""
    top_p: float = 1
    """Total probability mass of tokens to consider at each step."""
    stream: bool = False
    """Whether to stream the results or not."""
    frequency_penalty: float = 0
    """Penalizes repeated tokens according to frequency."""
    presence_penalty: float = 0
    """Penalizes repeated tokens."""
    n: int = 1
    """How many completions to generate for each prompt."""

    # max_tokens: int = 3000
    # """The maximum number of tokens to generate in the completion.
    # # -1 returns as many tokens as possible given the prompt and
    # # the models maximal context size."""

    def __call__(self, prompt, *args, **kwargs):
        llm_prompt = LLMPrompt(messages=[
            SystemMessage(content="You are a helpful AI assistant."),
            UserMessage(content=prompt)
        ])
        return self.generate_prompt(llm_prompt).content

    def generate_prompt(self, prompts: LLMPrompt) -> Optional[AssistantMessage]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CFG.openai_api_key}"
        }
        body = {
            "messages": self._parse_prompt(prompts),
        }
        body.update(self.__dict__)
        response = requests.post(url=CFG.get_request_url(), headers=headers, json=body)
        if response.status_code == 200:
            # todo enable stream mode
            # for chunk in response.iter_content(chunk_size=None):
            #     print(chunk)
            ret_data = response.json()
            logger.debug(f"[prompt_me] {ret_data}")
            content = ret_data['choices'][0]['message']['content']
            return AssistantMessage(content=content)

        logger.error("Failed to get data. Please check your network or api key.")
        return AssistantMessage(content="Failed to get data.")

    def _parse_prompt(self, prompts: LLMPrompt) -> List[dict]:
        converted_messages: List[dict] = []
        for message in prompts.messages:
            converted_messages.append({
                "role": message.type,
                "content": message.content
            })
        return converted_messages


# todo commit时删掉这里
def main():
    import os
    os.environ['OPENAI_API_KEY'] = "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"

    data = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, Who are you?"},
    ]
    openai = OpenAI()
    data = [
        SystemMessage(content="You are a helpful AI assistant."),
        UserMessage(content="你知道《只因你太美》吗？")
    ]
    openai_prompt = OpenAIPrompt(messages=data)
    print(openai.generate_prompt(openai_prompt).content)


if __name__ == '__main__':
    main()
