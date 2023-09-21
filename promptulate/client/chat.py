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
import questionary

from promptulate import Conversation
from promptulate.agents import ToolAgent
from promptulate.llms import ErnieBot, ChatOpenAI, BaseLLM
from promptulate.schema import LLMType
from promptulate.tools import (
    Calculator,
    DuckDuckGoTool,
    PythonREPLTool,
    ArxivQueryTool,
    SleepTool,
    HumanFeedBackTool,
)
from promptulate.tools.shell import ShellTool
from promptulate.utils import set_proxy_mode, print_text

MODEL_MAPPING = {"OpenAI": ChatOpenAI, "ErnieBot": ErnieBot}
TOOL_MAPPING = {
    "Calculator": Calculator,
    "WebSearch": DuckDuckGoTool,
    "Python Script Executor": PythonREPLTool,
    "Arxiv Query": ArxivQueryTool,
    "Sleep": SleepTool,
    "Shell Executor": ShellTool,
    "HumanFeedBackTool": HumanFeedBackTool,
}


def get_user_input() -> Optional[str]:
    marker = (
        "# You input are here (please delete this line)\n"
        "You should save it and close the notebook after writing the prompt. (please delete this line)\n"
    )
    message = click.edit(marker)
    if message is not None:
        return message
    return None


def simple_chat(llm: BaseLLM):
    conversation = Conversation(llm=llm)

    while True:
        print_text("[User] ", "blue")
        prompt = get_user_input()
        if not prompt:
            ValueError("Your prompt is None, please input something.")
        print_text(prompt, "blue")
        ret = conversation.run(prompt)
        print_text(f"[output] {ret}", "green")


def web_chat(llm: BaseLLM):
    if llm.llm_type == LLMType.ErnieBot:
        while True:
            print_text("[User] ", "blue")
            prompt = get_user_input()
            if not prompt:
                ValueError("Your prompt is None, please input something.")
            print_text(prompt, "blue")
            ret = llm(prompt)
            print_text(f"[agent] {ret}", "green")

    else:
        agent = ToolAgent(tools=[DuckDuckGoTool()], llm=llm)
        while True:
            print_text("[User] ", "blue")
            prompt = get_user_input()
            if not prompt:
                ValueError("Your prompt is None, please input something.")
            print_text(prompt, "blue")
            ret = agent.run(prompt)
            print_text(f"[agent] {ret}", "green")


def agent_chat(agent: ToolAgent):
    while True:
        print_text("[User] ", "blue")
        prompt = get_user_input()
        if not prompt:
            ValueError("Your prompt is None, please input something.")
        print_text(prompt, "blue")
        ret = agent.run(prompt)
        print_text(f"[agent] {ret}", "green")


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

    print_text(f"Hi there, here is promptulate chat terminal.", "pink")

    terminal_mode = questionary.select(
        "Choose a chat terminal:",
        choices=["Simple Chat", "Agent Chat", "Web Agent Chat"],
    ).ask()

    model = questionary.select(
        "Choose a llm model:",
        choices=list(MODEL_MAPPING.keys()),
    ).ask()
    # todo check whether exist llm key

    llm = MODEL_MAPPING[model](temperature=0.2)
    if terminal_mode == "Simple Chat":
        simple_chat(llm)
    elif terminal_mode == "Agent Chat":
        str_tools = questionary.checkbox(
            "Choose tools you want:", choices=list(TOOL_MAPPING.keys())
        ).ask()
        tools = []
        for str_tool in str_tools:
            tools.append(TOOL_MAPPING[str_tool]())
        agent = ToolAgent(tools=tools, llm=llm)
        agent_chat(agent)
    elif terminal_mode == "Web Agent Chat":
        web_chat(llm)


def main():
    chat()


if __name__ == "__main__":
    main()
