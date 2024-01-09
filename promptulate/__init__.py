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

import warnings

from promptulate.agents.base import BaseAgent
from promptulate.agents.tool_agent.agent import ToolAgent
from promptulate.agents.web_agent.agent import WebAgent
from promptulate.chat import chat
from promptulate.llms.base import BaseLLM
from promptulate.llms.openai.openai import ChatOpenAI
from promptulate.output_formatter import OutputFormatter
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    MessageSet,
    SystemMessage,
    UserMessage,
)
from promptulate.tools.base import BaseTool, Tool, define_tool
from promptulate.utils.logger import enable_log
from promptulate.utils.string_template import StringTemplate

_util_fields = [
    "enable_log",
    "OutputFormatter",
    "StringTemplate",
]

_schema_fields = [
    "AssistantMessage",
    "SystemMessage",
    "UserMessage",
    "BaseMessage",
    "MessageSet",
]

_llm_fields = [
    "chat",
    "BaseLLM",
    "ChatOpenAI",
]

_tool_fields = [
    "Tool",
    "define_tool",
    "BaseTool",
]

_agent_fields = [
    "BaseAgent",
    "WebAgent",
    "ToolAgent",
]

__all__ = [
    *_util_fields,
    *_schema_fields,
    *_llm_fields,
    *_tool_fields,
    *_agent_fields,
]

warnings.filterwarnings("always", category=DeprecationWarning)
