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
from typing import Optional, List, Union

from promptulate import utils
from promptulate.config import Config
from promptulate.frameworks.mixins import SummarizerMixin
from promptulate.preset_roles import BaseRole, DefaultRole
from promptulate.frameworks.schema import BaseConversationFramework, BasePromptFramework
from promptulate.schema import (
    SystemMessage,
    UserMessage,
    BaseMessage,
    AssistantMessage,
    LocalCacheChatMessageHistory,
    BaseChatMessageHistory
)

cache = utils.get_cache()
logger = utils.logger()


def get_message_from_cache(conversation_id) -> LocalCacheChatMessageHistory:
    pass
