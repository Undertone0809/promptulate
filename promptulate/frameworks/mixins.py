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

from pydantic import BaseModel, root_validator
from typing import List, Optional, Union, Any

from promptulate.schema import BaseMessage, BaseChatMessageHistory

"""
  Store: {
    DefaultTopic: "新的聊天",
    BotHello: "有什么可以帮你的吗",
    Error: "出错了，稍后重试吧",
    Prompt: {
      History: (content: string) =>
        "这是 ai 和用户的历史聊天总结作为前情提要：" + content,
      Topic:
        "使用四到五个字直接返回这句话的简要主题，不要解释、不要标点、不要语气词、不要多余文本，如果没有主题，请直接返回“闲聊”",
      Summarize:
        "简要总结一下你和用户的对话，用作后续的上下文提示 prompt，控制在 200 字以内",
    },
  },
"""


class translatorMixin(BaseModel):
    pass


class SummarizerMixin(BaseModel):
    """message summary capability provider"""

    # def predict_new_summary(
    #         self, messages: List[BaseMessage], existing_summary: str
    # ) -> str:
    #     new_lines = get_buffer_string(
    #         messages,
    #         human_prefix=self.human_prefix,
    #         ai_prefix=self.ai_prefix,
    #     )
    #
    #     chain = LLMChain(llms=self.llms, prompt=self.prompt)
    #     return chain.predict(summary=existing_summary, new_lines=new_lines)

    def summary_content(self):
        pass

    def summary_topic(self):
        pass


class DeriveHistoryMessageMixin(BaseModel):

    def get_history_messages(self):
        pass

    def output(self):
        pass


class StorageHistoryMessageMixin(BaseModel):
    pass
