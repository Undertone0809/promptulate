# 快速开始

## 安装最新版

打开终端，输入下面命令下载`promptulate`最新版，`-U`表示更新到最新版，如果你已经下载`promptulate`
旧版本，那么执行此命令会更新到最新版。`promptulate`当前正处于快速发展阶段，因此你可能需要经常更新最新版以享用最新的成果。

```shell script
pip install -U promptulate  
```

## 基本使用

> 下列教程全部使用`OPENAI gpt-3.5-turbo`进行测试

该部分将会介绍`promptulate`中一些常用组件的基本使用，带你快速了解`promptulate`的架构组成，快速上手部分仅仅提供最简单的使用，如果你有开发复杂应用程序的需求，请跳转至各个模块进行功能的详细阅读。


### KEY配置

在使用`promptulate`之前，你需要先导入你的`OPENAI_API_KEY`

```python
import os

os.environ['OPENAI_API_KEY'] = "your-key"
```

在你第一次使用的时候，需要使用`os.environ["OPENAI_API_KEY"]` 导入"OPENAI_API_KEY"
的环境变量，但是在第一运行之后`promptulate`
会进行缓存，即后面再运行就不需要再导入key了。如果你的key过期了，可以尝试重新按照上面的方法导入key，或者你也可以把`cache`
文件给删除掉，Windows的`cache`在当前目录下，linux的`cache`在`/tmp`下。

### LLM

> 详细文档请跳转[LLM](modules/llm.md#llm)

`promptulate`的架构设计可以轻松兼容不同的大语言模型扩展，在`promptulate`中，llm负责最基本的内容生成部分，因此为最基础的组件。

下面的示例展示了如何使用OpenAI进行交互。

```python
from promptulate.llms import ChatOpenAI

llm = ChatOpenAI()
answer = llm("请解释一下引力波的放射与广义相对论的必然关系")
print(answer)

```

输出结果如下：

```text
广义相对论是一种描述引力如何影响时空的物理学理论，它指出当物质和能量聚集在一起时，它们弯曲了周围的时空，引起了引力。质量和能量更大的物体会导致更大
的时空弯曲，这就是为什么地球会围绕太阳旋转。根据广义相对论，当物质或能量在空间中运动时，它们会产生引力波，就像在水面上产生涟漪一样。引力波是一种类
似电磁波的波动，但它们是由物质和能量的弯曲引起的，而电磁波是由电荷的振动引起的。引力波是极微弱的，但是当强烈的引力场存在（例如在引力天体碰撞或超新
星爆炸等事件中），它们可以被探测到。事实上，2015年，激光干涉引力波天文台利用引力波探测器直接探测到了引力波，并为广义相对论提供了强有力的证据。因
此，引力波的放射与广义相对论必然关系紧密。通过引力波，我们可以更加深入地了解时空的性质，并进一步验证这个理论。
```

### proxy

我想你可能遇到了无法访问的小问题，It's OK, `promptulate` 提供了三种访问OpenAI的方式，分别是

- `off` 默认的访问方式，不开代理
- `custom` 自定义代理方式
- `promptulate` promptulate提供的免费代理服务器

`promptulate` 提供了免费的代理服务器，感谢 [ayaka14732](https://github.com/ayaka14732/)
，你可以在不用科学上网的情况下直接调用OpenAI的相关接口，下面是三种代理的设置方式：

```python
from promptulate.llms import OpenAI
from promptulate.utils import set_proxy_mode


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
    answer = llm("请解释一下引力波的放射与广义相对论的必然关系")
    print(answer)


if __name__ == '__main__':
    main()
```

> 和OPENAI_API_KEY一样，关于代理的配置我也设置了缓存，这意味着你只需要配置一次代理即可(我也太聪明了吧)。事实上`promptulate`
> 提供了关闭全局配置项缓存的功能，但默认开启，不推荐关闭，所以我不告诉你怎么关闭，关闭了下面key池的重磅功能你将无法使用。

### Key池

`promptulate`为OpenAI进行特别优化，构建了Key池，如果你使用的是`GPT3.5`
5美元的账号，一定会遇到限速的问题，这个时候，如果你有一堆Key，就可以很好的解决这个问题。`promptulate`的LRU
KEY轮询机制巧妙的解决了限速的问题，你可以使用LLM随意地进行提问（前提是你有够多的key）。此外，如果你既有`GPT4`和`GPT3.5`
的KEY，KEY池也可以不同模型的KEY调度，你可以按照下面的方式将key导入到你的key池中。

```python
from promptulate.llms import OpenAI
from promptulate.utils import export_openai_key_pool

keys = [
    {"model": "gpt-3.5-turbo", "key": "xxxxx"},
    {"model": "gpt-3.5-turbo", "key": "xxxxx"},
    {"model": "gpt-3.5-turbo", "key": "xxxxx"},
    {"model": "gpt-4", "key": "xxxxx"},
]

export_openai_key_pool(keys)

llm = OpenAI()
for i in range(10):
    llm("你好")
```

### 简易终端

`promptulate`为大语言模型对话提供了一个简易终端，在你安装了了 `promptulate` 之后，你可以非常方便的使用这个简易终端进行一些对话，使用方式如下：

- 打开终端控制台，输入以下命令，就可以开启一个简易的对话

```shell
promptulate-chat --openai_api_key your_key_here --proxy_mode promptulate
```

```text

--openai_api_key 你的openai_api_key
--proxy_mode 代理模式，当前暂时只支持off和promptulate模式，如果你选择promptulate模式，你会发现你不用科学の上网也能访问，这是因为promptulate内置了代理。（后面会详细介绍）

```

- 当然并不是每次运行都要输入这么长的内容，因为在你第一次运行终端之后 `promptulate`
  会对你的配置信息进行缓存，因此下一次运行的时候，你只需要输入下面的命令就可以开始一段对话了

```shell
promptulate-chat
```

- 然后你就可以

```text
Hi there, here is promptulate chat terminal.
[User] 你好
[output] 你好！有什么我可以帮助你的吗？
[User] 只因你太美
[output] 谢谢夸奖，但作为一个语言模型，我没有真正的美丽，只有能力提供信息和帮助。那么，有什么问题或者需求我可以帮你解决 吗？
[User] 这真是太棒了
[output] 很高兴你觉得如此，我会尽力为您提供最佳的服务。有任何需要帮助的问题，请尽管问我。
```

> 需要注意的是，当前client只支持OpenAI的LLM，后续将会开放更多LLM，详情请查看[开发计划](other/plan.md)

### Conversation

上面展示的LLM组件，只提供了最基础的对话生成内容，但是其并不提供上下文对话、文章总结、角色预设等更加复杂的功能，所以接下来我们介绍功能更为强大的`Conversation`。

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
from promptulate.memory import FileChatMemory
from promptulate.llms import OpenAI


def main():
    memory = FileChatMemory()
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

上面的示例中，我们使用

- `FileChatMemory()`进行聊天记录的本地化文件存储，文件存储形式默认是以json的形式进行存储的，保存在`cache`中。
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
    name: str = "心灵导师"
    description: str = """
    从现在起你是一个充满哲学思维的心灵导师，当我每次输入一个疑问时你需要用一句富有哲理的名言警句来回答我，并且表明作者和出处
    要求字数不少于15个字，不超过30字，每次只返回一句且不输出额外的其他信息，你需要使用中文和英文双语输出"""


def main():
    role = SpiritualTeacher()
    conversation = Conversation(role=role)
    ret = conversation.predict("论文被拒绝了怎么办？")
    print(ret)
```