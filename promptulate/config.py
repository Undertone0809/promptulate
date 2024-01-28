# Copyright (c) 2023 promptulate
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

import os
from typing import Optional

import requests
from dotenv import load_dotenv

from promptulate.hook.stdout_hook import StdOutHook
from promptulate.utils.core_utils import get_cache
from promptulate.utils.logger import logger
from promptulate.utils.openai_key_pool import OpenAIKeyPool
from promptulate.utils.singleton import Singleton

PROXY_MODE = ["off", "custom", "promptulate"]
load_dotenv()


def set_enable_cache(value: bool):
    """Caching is enabled by default. Disabling caching is not recommended."""
    Config().enable_cache = value


def turn_off_stdout_hook():
    Config().turn_off_stdout_hook()


class Config(metaclass=Singleton):
    """
    Configuration class for managing application settings.

    Attributes:
        enable_cache (bool): Flag indicating whether caching is enabled.
        _proxy_mode (str): The current proxy mode.
        _proxies (Optional[dict]): Dictionary of proxy settings.
        openai_chat_api_url (str): URL for OpenAI chat API.
        openai_completion_api_url (str): URL for OpenAI completion API.
        openai_proxy_url (str): URL for OpenAI proxy.
        ernie_bot_url (str): URL for Ernie bot API.
        ernie_bot_turbo_url (str): URL for Ernie bot turbo API.
        ernie_bot_token_url (str): URL for Ernie bot token API.
        ernie_bot_4_url (str): URL for Ernie bot 4 API.
        ernie_embedding_v1_url (str): URL for Ernie embedding v1 API.
        key_default_retry_times (int): Default number of key retry times.
        enable_stdout_hook (bool): Flag indicating whether stdout hook is enabled.
    """

    def __init__(self):
        logger.info("[pne config] Config initialization")
        self.enable_cache: bool = True
        self._proxy_mode: str = PROXY_MODE[0]
        self._proxies: Optional[dict] = None

        self.openai_chat_api_url = "https://api.openai.com/v1/chat/completions"
        self.openai_completion_api_url = "https://api.openai.com/v1/completions"
        self.openai_proxy_url = "https://chatgpt-api.shn.hk/v1/"  # FREE API

        self.ernie_bot_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
        self.ernie_bot_turbo_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant"
        self.ernie_bot_token_url = "https://aip.baidubce.com/oauth/2.0/token"
        self.ernie_bot_4_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro"
        self.ernie_embedding_v1_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1"

        self.zhipu_model_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

        self.key_default_retry_times = 5
        """If llm(like OpenAI) unable to obtain data, retry request until the data is obtained."""  # noqa: E501
        self.enable_stdout_hook = True

        if self.enable_stdout_hook:
            StdOutHook.registry_stdout_hooks()

    def turn_off_stdout_hook(self):
        if self.enable_stdout_hook:
            self.enable_stdout_hook = False
            StdOutHook.unregister_stdout_hooks()

    def get_openai_api_key(self, model: str = "gpt-3.5-turbo") -> str:
        """Get openai key from KeyPool and environment variable. The priority of
        obtaining the key: environment variable, cache of OpenAIKeyPool, cache of
        OEPNAI_API_KEY."""
        if "OPENAI_API_KEY" in os.environ.keys():
            if self.enable_cache:
                get_cache()["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
            return os.getenv("OPENAI_API_KEY")

        if self.enable_cache:
            openai_key_pool: OpenAIKeyPool = OpenAIKeyPool()
            key = openai_key_pool.get(model)
            if key:
                return key

        if self.enable_cache and "OPENAI_API_KEY" in get_cache():
            return get_cache()["OPENAI_API_KEY"]

        raise ValueError("OPENAI API key is not provided. Please set your key.")

    def get_ernie_api_key(self) -> str:
        if "ERNIE_API_KEY" in os.environ.keys():
            if self.enable_cache:
                get_cache()["ERNIE_API_KEY"] = os.getenv("ERNIE_API_KEY")
            return os.getenv("ERNIE_API_KEY")
        if self.enable_cache and "ERNIE_API_KEY" in get_cache():
            return get_cache()["ERNIE_API_KEY"]
        raise ValueError("ERNIE_API_KEY is not provided. Please set your key.")

    @property
    def get_ernie_api_secret(self) -> str:
        if "ERNIE_API_SECRET" in os.environ.keys():
            if self.enable_cache:
                get_cache()["ERNIE_API_SECRET"] = os.getenv("ERNIE_API_SECRET")
            return os.getenv("ERNIE_API_SECRET")
        if self.enable_cache and "ERNIE_API_SECRET" in get_cache():
            return get_cache()["ERNIE_API_SECRET"]
        raise ValueError("ERNIE_API_SECRET is not provided. Please set your secret.")

    def get_zhipuai_api_key(self) -> str:
        if "ZHIPUAI_API_KEY" in os.environ.keys():
            if self.enable_cache:
                get_cache()["ZHIPUAI_API_KEY"] = os.getenv("ZHIPUAI_API_KEY")
            return os.getenv("ZHIPUAI_API_KEY")
        if self.enable_cache and "ZHIPUAI_API_KEY" in get_cache():
            return get_cache()["ZHIPUAI_API_KEY"]
        raise ValueError("ZHIPUAI_API_KEY is not provided. Please set your key.")

    def get_qianfan_ak(self):
        if "QIANFAN_ACCESS_KEY" in os.environ.keys():
            if self.enable_cache:
                get_cache()["QIANFAN_ACCESS_KEY"] = os.getenv("QIANFAN_ACCESS_KEY")
            return os.getenv("QIANFAN_ACCESS_KEY")
        if self.enable_cache and "QIANFAN_ACCESS_KEY" in get_cache():
            return get_cache()["QIANFAN_ACCESS_KEY"]
        raise ValueError("QIANFAN_ACCESS_KEY is not provided. Please set your key.")

    def get_qianfan_sk(self):
        if "QIANFAN_SECRET_KEY" in os.environ.keys():
            if self.enable_cache:
                get_cache()["QIANFAN_SECRET_KEY"] = os.getenv("QIANFAN_SECRET_KEY")
            return os.getenv("QIANFAN_SECRET_KEY")
        if self.enable_cache and "QIANFAN_SECRET_KEY" in get_cache():
            return get_cache()["QIANFAN_SECRET_KEY"]
        raise ValueError("QIANFAN_SECRET_KEY is not provided. Please set your secret.")

    def get_ernie_token(self) -> str:
        url = self.ernie_bot_token_url
        params = {
            "grant_type": "client_credentials",
            "client_id": self.get_ernie_api_key(),
            "client_secret": self.get_ernie_api_secret,
        }
        return str(requests.post(url, params=params).json().get("access_token"))

    def get_key_retry_times(self, model: str) -> int:
        if self.enable_cache:
            openai_key_pool: OpenAIKeyPool = OpenAIKeyPool()
            return openai_key_pool.get_num(model)
        return self.key_default_retry_times

    @property
    def proxy_mode(self) -> str:
        if self.enable_cache and "PROXY_MODE" in get_cache():
            return get_cache()["PROXY_MODE"]
        return self._proxy_mode

    @proxy_mode.setter
    def proxy_mode(self, value):
        self._proxy_mode = value
        if self.enable_cache:
            get_cache()["PROXY_MODE"] = value

    @property
    def proxies(self) -> Optional[dict]:
        if self.enable_cache and "PROXIES" in get_cache():
            return get_cache()["PROXIES"] if self.proxy_mode == "custom" else None
        return self._proxies

    @proxies.setter
    def proxies(self, value):
        self._proxies = value
        if self.enable_cache:
            get_cache()["PROXIES"] = value

    @property
    def openai_chat_request_url(self) -> str:
        if self.proxy_mode == PROXY_MODE[2]:
            self.proxies = None
            return self.openai_proxy_url
        return self.openai_chat_api_url

    @property
    def openai_completion_request_url(self) -> str:
        if self.proxy_mode == PROXY_MODE[2]:
            self.proxies = None
            return f"{self.openai_proxy_url}completions"
        return self.openai_completion_api_url

    def set_proxy_mode(self, mode: str, proxies: Optional[dict] = None):
        self.proxy_mode = mode
        self.proxies = proxies
        logger.info(f"[pne] proxy mode: {mode}, proxies: {proxies}")


pne_config = Config()
