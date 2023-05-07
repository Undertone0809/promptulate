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
from prompt_me.preset_role import BaseRole
from prompt_me import Conversation

os.environ['OPENAI_API_KEY'] = "your_key"


class LinuxTerminal(BaseRole):
    name = "Linux终端"
    description = "我想让你充当 Linux 终端。我将输入命令，您将回复终端应显示的内容。我希望您只在一个唯一的代码块内回复终端输出，而不" \
                  "是其他任何内容。不要写解释。除非我指示您这样做，否则不要键入命令。当我需要用英语告诉你一些事情时，我会把文字放在中括号内[就像这样]。"


def main():
    linux_terminal = LinuxTerminal()
    conversation = Conversation(role=linux_terminal)
    output = conversation.predict(msg="[ls]")
    print(f"[output] {output}")
    output = conversation.predict(msg="[cd /usr/local]")
    print(f"[output] {output}")


if __name__ == '__main__':
    main()
