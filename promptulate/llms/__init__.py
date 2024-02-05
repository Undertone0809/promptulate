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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from promptulate.llms.base import BaseLLM
    from promptulate.llms.erniebot.erniebot import ErnieBot
    from promptulate.llms.openai import ChatOpenAI, OpenAI
    from promptulate.llms.qianfan import QianFan
    from promptulate.llms.zhipu import ZhiPu


def __getattr__(name):
    if name == "BaseLLM":
        from promptulate.llms.base import BaseLLM

        return BaseLLM
    elif name == "ErnieBot":
        from promptulate.llms.erniebot.erniebot import ErnieBot

        return ErnieBot
    elif name == "ChatOpenAI":
        from promptulate.llms.openai import ChatOpenAI

        return ChatOpenAI
    elif name == "OpenAI":
        from promptulate.llms.openai import OpenAI

        return OpenAI
    elif name == "QianFan":
        from promptulate.llms.qianfan import QianFan

        return QianFan
    elif name == "ZhiPu":
        from promptulate.llms.zhipu import ZhiPu

        return ZhiPu


__all__ = ["OpenAI", "ChatOpenAI", "BaseLLM", "ErnieBot", "QianFan", "ZhiPu"]
