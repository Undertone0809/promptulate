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

from promptulate.agents.assistant_agent.agent import AssistantAgent
from promptulate.agents.base import BaseAgent
from promptulate.agents.planner.planner import Planner
from promptulate.agents.tool_agent.agent import ToolAgent
from promptulate.agents.web_agent.agent import WebAgent
from promptulate.chat import AIChat, Mode, chat
from promptulate.llms.base import BaseLLM
from promptulate.llms.factory import LLMFactory
from promptulate.llms.openai.openai import ChatOpenAI
from promptulate.output_formatter import OutputFormatter
from promptulate.schema import (
    AssistantMessage,
    BaseMessage,
    MessageSet,
    SystemMessage,
    UserMessage,
)
from promptulate.tools.base import BaseTool, Tool, ToolTypes, define_tool
from promptulate.utils.string_template import StringTemplate

_util_fields = [
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

_llm_fields = ["chat", "AIChat", "BaseLLM", "ChatOpenAI", "LLMFactory", "Mode"]

_tool_fields = [
    "Tool",
    "define_tool",
    "BaseTool",
    "ToolTypes",
]

_agent_fields = [
    "BaseAgent",
    "WebAgent",
    "ToolAgent",
    "AssistantAgent",
    "Planner",
]

__all__ = [
    *_util_fields,
    *_schema_fields,
    *_llm_fields,
    *_tool_fields,
    *_agent_fields,
]

warnings.filterwarnings("always", category=DeprecationWarning)
