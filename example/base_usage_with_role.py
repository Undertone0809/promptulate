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

import os
from prompt_me.preset_role import CopyWriter
from prompt_me import Conversation

os.environ['OPENAI_API_KEY'] = "your_key"


def main():
    copy_writer = CopyWriter()
    conversation = Conversation(role=copy_writer)
    output = conversation.predict(msg="你好,请问你是谁？")
    print(f"[output] {output}")
    output = conversation.predict(msg="请问你可以做什么？")
    print(f"[output] {output}")


if __name__ == '__main__':
    main()
