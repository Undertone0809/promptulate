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

from promptulate.agents import ToolAgent
from promptulate.config import Config
from promptulate.llms import BaseLLM, ChatOpenAI, ErnieBot
from promptulate.schema import LLMType, MessageSet
from promptulate.tools import (
    ArxivQueryTool,
    Calculator,
    DuckDuckGoTool,
    HumanFeedBackTool,
    PythonREPLTool,
    SleepTool,
)
from promptulate.tools.shell import ShellTool
from promptulate.utils.color_print import print_text
from promptulate.utils.proxy import set_proxy_mode

CFG = Config()
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
        "You should save it and close the notebook after writing the prompt. (please delete this line)\n"  # noqa
        "Reply 'exit' to exit the chat.\n"
    )
    message = click.edit(marker)

    if message == "exit":
        exit()

    return message


def get_user_openai_api_key():
    import os

    api_key = questionary.password("Please enter your OpenAI API Key: ").ask()
    os.environ["OPENAI_API_KEY"] = api_key


def simple_chat(llm: BaseLLM):
    messages = MessageSet(messages=[])

    while True:
        print_text("[User] ", "blue")
        prompt = get_user_input()

        if not prompt:
            ValueError("Your prompt is None, please input something.")

        print_text(prompt, "blue")
        messages.add_user_message(prompt)

        answer = llm.predict(messages)
        messages.add_message(answer)

        print_text(f"[output] {answer.content}", "green")


def web_chat(llm: BaseLLM, model: str):
    if llm.llm_type == LLMType.ErnieBot:
        llm = ErnieBot(model=model, temperature=0.1, disable_search=False)
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
    # get parameters
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

    print_text("Hi there, here is promptulate chat terminal.", "pink")

    terminal_mode = questionary.select(
        "Choose a chat terminal:",
        choices=["Simple Chat", "Agent Chat", "Web Agent Chat", "exit"],
    ).ask()

    if terminal_mode == "exit":
        exit(0)

    model = questionary.select(
        "Choose a llm model:",
        choices=[
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-3.5-turbo-16k",
            "ernie-bot-turbo",
            "ernie-bot",
            "ernie-bot-4",
        ],
    ).ask()

    # init model
    if "gpt" in model:
        llm = ChatOpenAI(model=model, temperature=0.0)
    elif "ernie" in model:
        llm = ErnieBot(model=model, temperature=0.1)

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
        web_chat(llm, model)


def main():
    chat()


if __name__ == "__main__":
    main()
