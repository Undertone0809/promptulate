import json
from typing import Optional, Any, Dict

import requests

from promptulate.config import Config
from promptulate.llms.base import BaseLLM
from promptulate.preset_roles.prompt import PRESET_SYSTEM_PROMPT_ZH
from promptulate.schema import (
    LLMPrompt,
    UserMessage,
    SystemMessage,
    AssistantMessage,
    parse_llm_prompt_to_dict,
)
from promptulate.utils.logger import get_logger

CFG = Config()
logger = get_logger()


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
    api_param_keys = [
        "model",
        "temperature",
        "top_p",
        "stream",
        "frequency_penalty",
        "presence_penalty",
        "n",
    ]
    """The key of openai api parameters"""
    preset_description: str = ""
    """OpenAI system message"""
    enable_private_api_key = False
    """Enable to provide a separate api for openai llm """
    private_api_key: str = ""
    """Store private api key"""
    # todo finish enable retry
    enable_retry: bool = True
    """Retry if API failed to get response. You can enable retry when you have a rate limited API."""
    retry_times: int = 5
    """If llm(like OpenAI) unable to obtain data, retry request until the data is obtained. You should
    enable retry if you want to use retry times."""
    retry_counter: int = 0
    """Used in conjunction with retry_times. Refresh when get data successfully."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.retry_times = CFG.get_key_retry_times(self.model)

    def __call__(self, prompt: str, *args, **kwargs) -> str:
    system_message = (
        self.preset_description
        if self.preset_description != ""
        else PRESET_SYSTEM_PROMPT_ZH
    )
    llm_prompt = LLMPrompt(
        messages=[
            SystemMessage(content=system_message),
            UserMessage(content=prompt),
        ]
    )
        return self.generate_prompt(llm_prompt).content

    def generate_prompt(self, prompts: LLMPrompt) -> Optional[AssistantMessage]:
        api_key = self.api_key
        logger.debug(f"[promptulate openai key] {api_key}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        body: Dict[str, Any] = self._build_api_params_dict(prompts)

        logger.debug(f"[promptulate openai params] body {body}")
        logger.debug(
            f"[promptulate openai request] url: {CFG.openai_request_url} proxies: {CFG.proxies}"
        )
        response = requests.post(
            url=CFG.openai_request_url, headers=headers, json=body, proxies=CFG.proxies
        )
        if response.status_code == 200:
            # todo enable stream mode
            # for chunk in response.iter_content(chunk_size=None):
            #     logger.debug(chunk)
            self.retry_counter = 0
            ret_data = response.json()
            logger.debug(f"[promptulate openai response] {json.dumps(ret_data)}")
            content = ret_data["choices"][0]["message"]["content"]
            logger.debug(f"[promptulate openai answer] {content}")
            return AssistantMessage(content=content)

        logger.error(
            "[promptulate OpenAI] Failed to get data. Please check your network or api key."
        )
        logger.debug("[promptulate OpenAI] retry to get response")
        if self.enable_retry and self.retry_counter < self.retry_times:
            self.retry_counter += 1
            return self.generate_prompt(prompts)

        return AssistantMessage(content=response.content)

    @property
    def api_key(self):
        if self.enable_private_api_key and self.private_api_key != "":
            return self.private_api_key
        return CFG.get_openai_api_key(self.model)

    def set_private_api_key(self, value: str):
        self.enable_private_api_key = True
        self.private_api_key = value

    def _build_api_params_dict(self, prompts: LLMPrompt) -> Dict[str, Any]:
    dic = {
        "messages": self._parse_prompt(prompts),
    }
    for key in self.api_param_keys:
        if key in self.__dict__:
            dic.update({key: self.__dict__[key]})
    return dic

    def _parse_prompt(self, prompts: LLMPrompt) -> List[Dict]:
        return parse_llm_prompt_to_dict(prompts)
