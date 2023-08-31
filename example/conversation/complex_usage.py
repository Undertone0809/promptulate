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

from promptulate import Conversation
from promptulate.llms import ChatOpenAI
from promptulate.memory import FileChatMemory


def main():
    memory = FileChatMemory()
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.9,
        top_p=1,
        stream=False,
        presence_penalty=0,
        n=1,
    )
    conversation = Conversation(llm=llm, memory=memory)
    ret = conversation.run("什么是引力波")
    print(f"[predict] {ret}")
    ret = conversation.predict_by_translate("请介绍一下引力波与广义相对论的必然关系", country="America")
    print(f"[translate output] {ret}")
    ret = conversation.summary_content()
    print(f"[summary content] {ret}")
    ret = conversation.summary_topic()
    print(f"[summary topic] {ret}")
    ret = conversation.export_message_to_markdown(
        output_type="file", file_path="output.md"
    )
    print(f"[export markdown] {ret}")


if __name__ == "__main__":
    main()
