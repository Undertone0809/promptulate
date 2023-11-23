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

__all__ = [
    "SUMMARY_CONTENT_PROMPT_ZH",
    "SUMMARY_TOPIC_PROMPT_ZH",
    "SUMMARY_TOPIC_PROMPT_EN",
    "SUMMARY_CONTENT_PROMPT_EN",
]

SUMMARY_CONTENT_PROMPT_ZH = """
简要总结一下你和用户的对话，用作后续的上下文提示 prompt，控制在 200 字以内
"""

SUMMARY_TOPIC_PROMPT_ZH = """
上面是ai 和用户的历史聊天总结作为前情提要，请使用四到五个字直接返回这句话的简要主题，
不要解释、不要标点、不要语气词、不要多余文本，如果没有主题，请直接返回“闲聊”
"""

SUMMARY_CONTENT_PROMPT_EN = """
Give a quick summary of your conversation with the user and use it as a follow-up context prompt, no more than 200 words
"""  # noqa

SUMMARY_TOPIC_PROMPT_EN = """
As the previous feed, please use four or five words to return directly to the brief topic of the sentence,
no explanation, no punctuation, no particles, no extra text, or if there is no topic, just return to "small talk".
"""  # noqa
