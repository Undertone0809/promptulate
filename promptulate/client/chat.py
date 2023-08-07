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

import argparse
import os
from typing import Optional

import click

from promptulate import Conversation
from promptulate.utils import set_proxy_mode


def get_user_input() -> Optional[str]:
    marker = (
        "# You input are here (please delete this line)\n"
        "You should save it and close the notebook after writing the prompt. (please delete this line)\n"
    )
    message = click.edit(marker)
    if message is not None:
        return message
    return None


def chat():
    parser = argparse.ArgumentParser(
        description="Welcome to Promptulate Chat - The best chat terminal ever!"
    )
    parser.add_argument(
        "--openai_api_key",
        help="when you first run, you should enter your openai api key",
    )
    parser.add_argument(
        "--proxy_mode", help="select openai proxy and provide [off, promptulate]"
    )
    args = parser.parse_args()

    if args.openai_api_key:
        os.environ["OPENAI_API_KEY"] = args.openai_api_key
    if args.proxy_mode:
        set_proxy_mode(args.proxy_mode)

    print(f"Hi there, here is promptulate chat terminal.")
    conversation = Conversation()
    while True:
        print("[User] ")
        prompt = get_user_input()
        if not prompt:
            ValueError("Your prompt is None, please input something.")
        print(prompt)
        ret = conversation.predict(prompt)
        print(f"[output] {ret}")


def main():
    chat()


if __name__ == "__main__":
    main()
