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
# Project Link: https://github.com/Undertone0809/prompt-me
# Contact Email: zeeland@foxmail.com

from prompt_me.llm import Message


def create_chat_message(role, content) -> Message:
    """
    Create a chat message with the given role and content.

    Args:
        role (str): The role of the message sender, e.g., "system", "user", or "assistant".
        content (str): The content of the message.

    Returns:
        dict: A dictionary containing the role and content of the message.
    """
    return {"role": role, "content": content}
