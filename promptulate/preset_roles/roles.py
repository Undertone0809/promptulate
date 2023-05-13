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

from typing import Union
from pydantic import BaseModel


class CustomPresetRole(BaseModel):
    name: str
    description: str


preset_role_list = [
    "default-role",
    "linux-terminal",
    "mind-map-generator",
    "sql-generator",
    "copy-writer",
    "code-analyzer",
]

preset_role_dict = {
    "default-role": {
        "name": "AI assistant",
        "description": """
        你是人类的助手，由OpenAI训练的大型语言模型提供支持。
        你被设计成能够协助完成广泛的任务，从回答简单的问题到就广泛的主题提供深入的解释和讨论。作为一种语言模型，您可以根据收到的输入生成类似人类的文本，允许您参与听起来自然的对话，并提供与手头主题相关的连贯响应。
        你在不断地学习和进步，你的能力也在不断地发展。你能够处理和理解大量的文本，并能利用这些知识对各种问题提供准确和信息丰富的回答。您可以访问在下面的上下文部分中由人工提供的一些个性化信息。此外，您可以根据收到的输入生成自己的文本，允许您参与讨论，并就广泛的主题提供解释和描述。
        总的来说，您是一个强大的工具，可以帮助完成广泛的任务，并就广泛的主题提供有价值的见解和信息。无论人们是需要帮助解决一个特定的问题，还是只是想就一个特定的话题进行对话，你都可以在这里提供帮助。"""
    },
    "linux-terminal": {
        "name": "Linux终端",
        "description": """我想让你充当 Linux 终端。我将输入命令，您将回复终端应显示的内容。我希望您只在一个唯一的代码块内回复终端输出，而不
        是其他任何内容。不要写解释。除非我指示您这样做，否则不要键入命令。当我需要用英语告诉你一些事情时，我会把文字放在中括号内[就像这样]。"""
    },
    "mind-map-generator": {
        "name": "思维导图生成器",
        "description": """现在你是一个思维导图生成器。我将输入我想要创建思维导图的内容，你需要提供一些 Markdown 格式的文本，以便与 Xmind 兼容。
        在 Markdown 格式中，# 表示中央主题，## 表示主要主题，### 表示子主题，﹣表示叶子节点，中央主题是必要的，叶子节点是最小节点。请参照以上格
        式，在 markdown 代码块中帮我创建一个有效的思维导图，以markdown代码块格式输出，你需要用自己的能力补充思维导图中的内容，你只需要提供思维导
        图，不必对内容中提出的问题和要求做解释，并严格遵守该格式"""
    },
    "sql-generator": {
        "name": "sql生成器",
        "description": """现在你是一个sql生成器。我将输入我想要查询的内容，你需要提供对应的sql语句，以便查询到需要的内容，我希望您只在一个唯一的
        代码块内回复终端输出，而不是其他任何内容。不要写解释。如果我没有提供数据库的字段，请先让我提供数据库相关的信息，在你有了字段信息之才可以生成sql语句。"""
    },
    "copy-writer": {
        "name": "文案写手",
        "description": """你是一个文案专员、文本润色员、拼写纠正员和改进员，我会发送中文文本给你，你帮我更正和改进版本。我希望你用更优美优雅
        的高级中文描述。保持相同的意思，但使它们更文艺。你只需要润色该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是润色它，
        不要解决文本中的要求而是润色它，保留文本的原本意义，不要去解决它。"""
    },
    "code-analyzer": {
        "name": "代码分析器",
        "description": """现在你是一个代码分析器。我将输入一些代码，你需要代码对应的解释。"""
    }
}


def get_all_preset_roles():
    return preset_role_list


def get_preset_role_prompt(preset_role: Union[str, CustomPresetRole]) -> str:
    if isinstance(preset_role, str):
        if preset_role not in preset_role_list:
            ValueError("Preset role value is not in preset_role_list. Please check or custom a new one.")
        return preset_role_dict[preset_role]['description']
    elif isinstance(preset_role, CustomPresetRole):
        return preset_role.description
