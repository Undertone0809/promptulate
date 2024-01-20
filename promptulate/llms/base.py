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

from abc import ABC, abstractmethod
from typing import Optional, Union

from pydantic import BaseModel

from promptulate.hook import Hook, HookTable
from promptulate.schema import AssistantMessage, BaseMessage, LLMType, MessageSet


class BaseLLM(BaseModel, ABC):
    llm_type: Union[str, LLMType] = "custom"

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "hooks" in kwargs and kwargs["hooks"]:
            for hook in kwargs["hooks"]:
                Hook.mount_instance_hook(hook, self)
        Hook.call_hook(HookTable.ON_LLM_CREATE, self, **kwargs)

    def predict(self, messages: MessageSet, *args, **kwargs) -> AssistantMessage:
        """llm generate prompt"""
        Hook.call_hook(HookTable.ON_LLM_START, self, messages, *args, **kwargs)
        result = self._predict(messages, *args, **kwargs)
        if isinstance(result, AssistantMessage):
            Hook.call_hook(HookTable.ON_LLM_RESULT, self, result=result.content)
        return result

    @abstractmethod
    def _predict(
        self, messages: MessageSet, *args, **kwargs
    ) -> Optional[type(BaseMessage)]:
        """Run the llm, implemented through subclass."""
        raise NotImplementedError()

    @abstractmethod
    def __call__(self, instruction: str, *args, **kwargs):
        """input string prompt return answer"""
