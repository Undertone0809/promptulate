<h1 align="center">
    Promptulate
</h1>


<p align="center">
    <a target="_blank" href="">
        <img src="https://img.shields.io/github/license/Undertone0809/promptulate.svg?style=flat-square" />
    </a>
    <a target="_blank" href=''>
        <img src="https://img.shields.io/github/release/Undertone0809/promptulate/all.svg?style=flat-square"/>
    </a>
    <a target="_blank" href=''>
        <img src="https://bestpractices.coreinfrastructure.org/projects/3018/badge"/>
   </a>
</p>

<p align="center">
  <img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/Snipaste_2023-05-13_17-37-23.png"/>
</p>



`promptulate` 是一个专为 Prompt Engineer设计LLM Prompt Layer框架，支持连续对话、对话保存、对话内容与标题总结、角色预设、使用外部工具等功能，开箱即用。
通过 `promptulate`，你可以轻松构建起属于自己的LLM应用程序。

本项目重构重构重构了两次，在本人深度阅读`langchain, Auto-GPT, django, django-rest-framework, gpt_academic...`
等大牛项目的源码之后，学习它们的架构、代码设计思路等内容，最终有了现在的版本，相较于之前的老版本`prompt-me`，`promptulate`
重新构建了 `llms, message, memory, framework, preset_roles, tools, provider`等模块，将`prompt`
的各个流程全部组件化，便有了现在的`promptualte`框架，但是工作量很大，还在不断地完善细节中，欢迎大家的参与。

# 特性

- 大语言模型支持：支持不同类型的大语言模型的扩展接口（当前暂时只支持GPT）
- 角色预设：提供预设角色，以不同的角度调用GPT
- 内置API代理，不用科学上网也可以直接使用
- 接口代理：支持调用ChatGPT API官方接口或自治代理
- 长对话模式：支持长对话聊天，支持多种方式的对话持久化
- 数据导出：支持markdowm等格式的对话导出
- 对话总结：提供API式的对话总结、翻译、标题生成
- 高级抽象，支持插件扩展、存储扩展、大语言模型扩展

# 基础架构

在看了当前这么多`prompt-engineering`之后，本人的架构设计思想在`langchain, Auto-GPT`
之上进行不断改进，构建出了一套属于`promptualte`的LLM Prompt Layer框架。`promptulate` 由以下几部分组成：

- Agent 更高级的执行器，负责复杂任务的调度和分发
- framework 框架层，实现不同类型的prompt框架，包括最基础的`Conversation`模型，还有`self-ask`和`ReAct`等模型正在火速开发中
- llm 大语言模型，负责生成回答，可以支持不同类型的大语言模型
- memory 负责对话的存储，支持不同的存储方式及其扩展，如文件存储、数据库存储等，相关扩展正在开发中
- tools 提供外部工具扩展调用，如搜索引擎、计算器等
- preset roles 提供预设角色，进行定制化对话
- provider 为framework和agent提供tools和其他细粒度能力的集成

# 快速上手

```shell script
pip install -U promptulate  
```

## 基本使用

> 后面的文档全部使用`OPENAI GPT3.5`进行测试

在使用`promptulate`之前，你需要先导入你的`OPENAI_API_KEY`

```python
import os

os.environ['OPENAI_API_KEY'] = "your-key"
```

在你第一次使用的时候，需要使用`os.environ["OPENAI_API_KEY"]` 导入"OPENAI_API_KEY"
的环境变量，但是在第一运行之后`promptulate`会进行缓存，即后面再运行就不需要再导入key了。如果你的key过期了，可以把`cache`
文件给删除掉，Windows的`cache`在当前目录下，linux的`cache`在`/tmp`下。

### LLM

`promptulate`的架构设计可以轻松兼容不同的大语言模型扩展，在`promptulate`中，llm负责最基本的内容生成部分，因此为最基础的组件。下面展示一个OpenAI的示例：

```python
from promptulate.llms import OpenAI

llm = OpenAI()
llm("你知道鸡哥的《只因你太美》？")
```

```text
'是的，鸡哥的《只因你太美》是这几年非常流行的一首歌曲。'
```

### proxy

我想你可能遇到了无法访问的小问题，It's OK, `promptulate` 提供了三种访问OpenAI的方式，分别是

- `off` 默认的访问方式，不开代理
- `custom` 自定义代理方式
- `promptulate` promptulate提供的免费代理服务器

`promptulate` 提供了免费的代理服务器，感谢 [ayaka14732](https://github.com/ayaka14732/)
，你可以在不用科学上网的情况下直接调用OpenAI的相关接口，下面是代理的设置方式：

```python
from promptulate.llms import OpenAI
from promptulate.utils import set_proxy_mode

llm = OpenAI()
llm("你知道鸡哥的《只因你太美》？")


def set_free_proxy():
    set_proxy_mode("promptulate")


def set_custom_proxy():
    proxies = {'http': 'http://127.0.0.1:7890'}
    set_proxy_mode("custom", proxies=proxies)


def turn_off_proxy():
    set_proxy_mode("off")


def main():
    set_free_proxy()
    llm = OpenAI()
    llm("你知道鸡哥的《只因你太美》？")

    
if __name__ == '__main__':
    main()
```

> 和OPENAI_API_KEY一样，关于代理的配置我也设置了缓存，这意味着你只需要配置一次代理即可(我也太聪明了吧)。事实上`promptulate`
> 提供了关闭全局配置项缓存的功能，但默认开启，不推荐关闭，所以我不告诉你怎么关闭~

### Conversation

`Conversation` 是`framework`中最基础的组件，其支持prompt生成、上下文对话、对话存储、角色预设的基本功能，此外，`provider`
为其提供了语言翻译、markdown数据导出、对话总结、标题总结等扩展功能。

接下来，我们先从对基础的对话开始，使用`Conversation`可以开始一段对话，使用其`predict()`函数可以生成回答。

```python
from promptulate import Conversation

conversation = Conversation()
conversation.predict("你知道鸡哥的《只因你太美》吗？")
```

```text
'是的，鸡哥的《只因你太美》是这几年非常流行的一首歌曲。'
```

`Conversation`默认使用`OpenAI GPT3.5`作为LLM，当然，因为其架构设计，`Conversation`
还可以轻松扩展其他类型的llm（当前暂时只开发了OpenAI，其他大语言模型的扩展正在火速开发中，当然如果你有自己想接入的大语言模型，欢迎你的pr！）

下面是一个更复杂的示例，展示了使用OpenAI作为大语言模型进行对话，使用本地文件进行存储，进行文章总结与标题总结的功能。

```python
from promptulate import Conversation
from promptulate.memory import LocalCacheChatMemory
from promptulate.llms import OpenAI


def main():
    memory = LocalCacheChatMemory()
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.9, top_p=1, stream=False, presence_penalty=0, n=1)
    conversation = Conversation(llm=llm, memory=memory)
    ret = conversation.predict("你知道鸡哥的著作《只因你太美》吗？")
    print(f"[predict] {ret}")
    ret = conversation.predict_by_translate("你知道鸡哥会什么技能吗？", country='America')
    print(f"[translate output] {ret}")
    ret = conversation.summary_content()
    print(f"[summary content] {ret}")
    ret = conversation.summary_topic()
    print(f"[summary topic] {ret}")
    ret = conversation.export_message_to_markdown(output_type="file", file_path="output.md")
    print(f"[export markdown] {ret}")


if __name__ == '__main__':
    main()

```

```text
[predict] 是的，我知道《只因你太美》这本书，是中国知名作家鸡肋（江南）所著的一篇言情小说。这本小说讲述了一个富家千金与一个贫穷男孩之间的爱情故事，情节曲折动人，深受读者喜爱。该小说在出版后得到了很高的评价和反响，并被改编成电影和电视剧等多种形式进行推广。
[translate output] I'm sorry, I cannot determine what you mean by "鸡哥" or what skills they may possess without additional context. Can you please provide more information or clarify your question?
[summary content] 在之前的对话中，用户询问我是否知道鸡哥的著作《只因你太美》。我回答了肯定的，解释了该小说的情节大致概括和其受欢迎的原因。我也提到了该小说的广泛影响，包括被改编成电影和电视剧等多种形式进行推广。
[summary topic] 鸡哥的小说。
```

> 咱就是说季皮提老师不懂鸡哥-.-

上面的示例中，我们使用

- `LocalCacheChatMemory()`进行聊天记录的本地化文件存储，文件存储形式默认是以json的形式进行存储的，保存在`cache`中。
- `OpenAI(model="gpt-3.5-turbo", temperature=0.9, top_p=1, stream=False, presence_penalty=0, n=1)`
  进行初始化一个大模型，里面是OpenAI需要传入的一些参数，具体可以查看[https://platform.openai.com/docs/api-reference/chat/create](https://platform.openai.com/docs/api-reference/chat/create)
  查看具体含义，这里不做详细讲解，如果你不想理会这些参数，你也可以直接`llm = OpenAI()`就好啦，默认使用`gpt-3.5-turbo`
  作为大语言模型，其他参数使用默认的就好了。
- `conversation.predict_by_translate("你知道鸡哥会什么技能吗？", country='America')`
  这个功能为使用特定语言进行预测，`provider`为其提供了`TranslatorMixin`，让`Conversation`
  得以拥有此功能。对于这个方法，你只需要传入prompt和你需要转换的语言的国家名称就好了。
- `conversation.summary_content()`这个函数可以直接总结上面的对话内容。
- `conversation.summary_topic()` 这个函数可以直接总结上面的对话，并提供一个标题。
- `conversation.export_message_to_markdown(output_type="file", file_path="output.md")`
  这个函数可以将对话记录导出为markdown文件，如果`output_type="text"`，则只返回markdown对话的内容。

`provider`为`Conversation`提供了 `SummarizerMixin, TranslatorMixin, DeriveHistoryMessageMixin`
，让其拥有了总结对话、总结标题、翻译、markdown导出的能力，provider提供的函数中一般都提供了一个`enable_embed_message`
的参数，这个参数的意思是：是否将本次对话保存进历史对话中，下面我们来看一个demo。

```python
from promptulate import Conversation

conversation = Conversation()
conversation.predict_by_translate("你知道鸡哥会什么技能吗？", country='America', enable_embed_message=True)
```

如果你设置了`enable_embed_message=True`, 那么这一次的predict将保存进历史对话中，provider提供的函数默认是不会将预测结果存入对话中的哦，这一点需要注意一下。

### 角色预设

你可以为`framework`提供一些特定的角色，让其可以处理特殊任务，如linux终端，思维导图生成器等，通过下面的方法你可以查看当前支持所有的预设角色。

```python
from promptulate.preset_roles import get_all_preset_roles

print(get_all_preset_roles())
```

> ['default-role', 'linux-terminal', 'mind-map-generator', 'sql-generator', 'copy-writer', 'code-analyzer']

下面展示使用`mind-map-generator`生成md思维导图的过程：

```python
from promptulate import Conversation


def main():
    conversation = Conversation(role="mind-map-generator")
    ret = conversation.predict("请帮我生成一段python的思维导图")
    print(ret)


if __name__ == '__main__':
    main()

```

```text
# Python
## 基础语法
### 数据类型
- 数字
- 字符串
- 列表
...
```

放入xmind中可以直接导入生成markdown的思维导图，咱就是说还不错，如下图所示：

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230513172038.png"/>

如果你想要自定义预设角色，可以使用如下方法：

```python
from promptulate import Conversation
from promptulate.preset_roles import CustomPresetRole


class SpiritualTeacher(CustomPresetRole):
    name = '心灵导师'
    description = """
    从现在起你是一个充满哲学思维的心灵导师，当我每次输入一个疑问时你需要用一句富有哲理的名言警句来回答我，并且表明作者和出处
    要求字数不少于15个字，不超过30字，每次只返回一句且不输出额外的其他信息，你需要使用中文和英文双语输出"""


def main():
    role = SpiritualTeacher()
    conversation = Conversation(role=role)
    ret = conversation.predict("论文被拒绝了怎么办？")
    print(ret)


if __name__ == '__main__':
    main()

```

```text
“失败不是终点，放弃才是。”——托马斯·爱迪生
```

# 待办清单

- 提供更多LLM模型支持
- 提供Agent进行复杂任务调度
- 提供更加方便的程序调用方式
- ~~添加角色预设~~
- 预设角色的参数配置
- 提供prompt模板与prompt结构化
- 提供外部工具扩展
    - 外部搜索： Google,Bing等
    - 可以执行shell脚本
    - 提供Python REPL
    - arvix论文工具箱，总结，润色
    - 本地文件总结
- 对话存储
    - 提供向量数据库存储
    - 提供mysql, redis等数据库存储
- 自建知识库建立专家决策系统
- 接入self-ask, prompt-loop架构
- 提供多种导出方式
- ~~可以导出历史消息为markdown格式~~
- ~~使用环境变量配置key~~
- 提供显示当前token（单词量）的功能
- ~~添加错误处理机制，如网络异常、服务器异常等，保证程序的可靠性~~
- ~~开发ChatBot v2, [issue](https://github.com/Undertone0809/cushy-chat/issues/1)~~
- 完善代理模式
- 提供gradio快速演示服务器
- ~~封装消息体，完善消息体中的信息~~
- ~~长对话自动/手动总结~~
- ~~提供全局配置的缓存开关~~
- Conversation传入convesation_id继续上次对话
- 提供修改local_cache默认位置的方法
- 为predict提供回调模式

> 妈呀，我怎么还有这么多待办事项，vivo50帮帮我 >.<

# 一些问题

- 本人正在尝试一些更加完善的抽象模式，以更好地兼容该框架，以及外部工具的扩展使用，如果你有更好的建议，欢迎一起讨论交流。

# 贡献

如果你想为这个项目做贡献，你可以提交pr或issue。我很高兴看到更多的人参与并优化它。