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
from promptulate import enable_log
from promptulate.llms import OpenAI, ErnieBot, ChatOpenAI

import os

from promptulate.tools import PaperSummaryTool

os.environ['ERNIE_API_KEY'] = "xxxxxx"
os.environ['ERNIE_API_SECRET'] = "xxxxxxx"
from promptulate.utils import export_openai_key_pool, set_proxy_mode

keys = [
    {"model": "gpt-3.5-turbo",
     "keys": "xx,xx"},
]

export_openai_key_pool(keys)


def set_free_proxy():
    set_proxy_mode("promptulate")


def turn_off_proxy():
    set_proxy_mode("off")


def main():
    # set_free_proxy()
    turn_off_proxy()
    # enable_log()
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9, top_p=1, stream=False, presence_penalty=0, n=1)
    llm = ErnieBot(model="ernie-bot")
   # llm = ChatOpenAI()
    prompt = """
    Please strictly output the following content.
    [start] This is a test [end]
    """
    result = llm(prompt, stop=["test","is"])
    #tool = PaperSummaryTool()
    #result = tool.run("attention is all you need")
    # you can also input an arxiv id as follows
    # result = tool.run("2303.09014")
    print(result)


if __name__ == "__main__":
    main()
