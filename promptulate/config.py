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

import os

from promptulate.utils.singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self):
        self.enable_proxy = True
        self.openai_url = 'https://api.openai.com/v1/chat/completions'
        self.proxy_url = 'https://chatgpt-api.shn.hk/v1/'  # FREE API

    @property
    def openai_api_key(self):
        if "OPENAI_API_KEY" not in os.environ.keys():
            raise ValueError('OPENAI API key is not provided')
        return os.getenv("OPENAI_API_KEY")

    def get_request_url(self) -> str:
        return self.proxy_url if self.enable_proxy else self.openai_url

    def set_enable_proxy(self, value: bool):
        self.enable_proxy = value
