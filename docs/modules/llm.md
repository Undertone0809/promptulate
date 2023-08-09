# LLM

### 简介

> 需要注意的是，`promptulate`中会把LLM与llm的意思分开来，LLM表示大语言模型，llm表示`promptulate`中的llm模块。

本文将会介绍llm模块的**基本使用方式，API KEY、KEY池、代理的配置方式**。

LLM指大语言模型，当前市面上常见的大语言模型有GPT3.5, GPT4, LLaMa, InstructGPT等大语言模型。`promptulate`可以支持不同类型的大语言模型调用。

当前`promptulate`重点适配了OpenAI的相关的大语言模型(GPT-3.5, GPT-4.0, text-davinci-003)，其他模型适配尚不成熟(文心一言、ChatGLM适配中)，正在开发中，因此下面的示例全部以OpenAI模型为例。如果你有想用的LLM或者更好的想法，欢迎提出你的想法。

### KEY配置

在使用`promptulate`之前，你需要先导入你的`OPENAI_API_KEY`

```python
import os

os.environ['OPENAI_API_KEY'] = "your-key"
```

在你第一次使用的时候，需要使用`os.environ["OPENAI_API_KEY"]` 导入"OPENAI_API_KEY" 的环境变量，但是在第一运行之后`promptulate` 会进行缓存，即后面再运行就不需要再导入key了。

如果你的key过期了，可以尝试重新按照上面的方法导入key，或者你也可以把`cache` 文件给删除掉，通过以下代码可以获取到缓存文件的位置:

```python
from promptulate.utils import get_default_storage_path

print(get_default_storage_path())
```



### LLM快速上手

`promptulate`的架构设计可以轻松兼容不同的大语言模型扩展，在`promptulate`中，llm负责最基本的内容生成部分，因此为最基础的组件。

下面的示例展示了如何使用OpenAI的大语言模型进行交互。

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

### LLM的类型

事实上，OpenAI的LLM模型分为 **文本推理型(text-davinci-003)** 和 **对话型(GPT3.5, GPT-4.0)** ，在`promptulate`中分别对应了`OpenAI`和`ChatOpenAI`。对于文本推理型LLM(OpenAI)，直接给定一段prompt，LLM会直接在prompt的后面进行补全，比如如果你的prompt是`你好！`，那么LLM会尝试直接在你的prompt的基础上进行文本推理，其输出可能为`你好！今天真是个好天气`。

```python
from promptulate.llms import OpenAI

llm = OpenAI()
answer = llm("你好")
print(answer)
```

输出如下所示：

```text
你好！今天真是个好天气
```

那么在大多数时候，这个结果并不是的我们想要的答案，我们想要让LLM成为一个机器人，因此，我们可以使用对话型LLM，即LLM的文本推理会以对话的形式展开，这个时候，我们的输入事实上并不是一段prompt，而是一段对话，LLM会根据历史的对话得出它的回复，下面是一个示例输入：

```json
[
    {
        "role": "system",
        "content": "Answer the following questions as best you can."
    },
    {
        "role": "user",
        "content": "Joe平均每分钟出拳25次。一场战斗持续5轮，每轮3分钟。他打了多少拳？ 让我们一步一步地思考。"
    },
    {
        "role": "assistant",
        "content": "好的，让我们来解决这个问题。 \n首先，一轮战斗持续3分钟，Joe每分钟出拳25次，那么一轮他出拳的次数是25乘以3等于75次。 \n接下来，我们将五轮的数量相加，即75乘以5等于 <<75*5=375>>375。 \n因此，Joe在这场战斗中打了375次拳。"
    },
    {
        "role": "user",
        "content": "请输出最终答案，你的输出格式为\n{answer}\n除此之外，不能输出其他任何内容，否则你将被惩罚。\n"
    }
]
```

这个时候，`gpt-3.5-turbo`输出可能为：

```json
[
    {
        "role": "system",
        "content": "Answer the following questions as best you can."
    },
    {
        "role": "user",
        "content": "Joe平均每分钟出拳25次。一场战斗持续5轮，每轮3分钟。他打了多少拳？ 让我们一步一步地思考。"
    },
    {
        "role": "assistant",
        "content": "好的，让我们来解决这个问题。 \n首先，一轮战斗持续3分钟，Joe每分钟出拳25次，那么一轮他出拳的次数是25乘以3等于75次。 \n接下来，我们将五轮的数量相加，即75乘以5等于 <<75*5=375>>375。 \n因此，Joe在这场战斗中打了375次拳。"
    },
    {
        "role": "user",
        "content": "请输出最终答案，你的输出格式为：\n{answer}\n除此之外，不能输出其他任何内容，否则你将被惩罚。\n"
    },
    {
        "role": "assistant",
        "content": "375"
    }
]
```

因此，如果你想使用GPT3.5，你可以按照如下方式使用：

```python
from promptulate.llms import ChatOpenAI

llm = ChatOpenAI()
result: str = llm("你好")
print(result)
```

输出结果如下所示：

```text
你好！有什么我可以帮助你的吗？
```

如果你想使用`GPT-4.0`，你只需要`ChatOpenAI(model="gpt-4.0")`进行初始化就可以了，默认情况下，使用`gpt-3.5-turbo`模型。

事实上，我们推荐你在大多数情况下使用`ChatOpenAI`，如果你是一个初级prompt engineer，那么文本推理型的LLM可能并不是那么适合你，相反，你可以轻松用`gpt-3.5-turbo`来构建复杂应用。

> 需要注意的是，OpenAI已经准备弃用text-davinci-003模型，因此你在调用OpenAI(text-davinci-003模型)的时候，会出现`"This model version is deprecated. Migrate before January 4, 2024 to avoid disruption of service. Learn more https://platform.openai.com/docs/deprecations`的警告。

### LLM自定义参数
对于大语言模型开发者来说，你或许知道OpenAI的GPT API提供了其他参数以便更好地调整GPT的输出特性，下面的示例展示了一个使用GPT4模型自定义参数的OpenAI模型初始化。

```python
from promptulate.llms import OpenAI

llm = OpenAI(model="gpt-4", temperature=0.9, top_p=1, stream=False, presence_penalty=0, n=1)
llm("请介绍一下引力波的放射与广义相对论的必然关系")
```

上面的示例中，使用`OpenAI(model="gpt-4", temperature=0.9, top_p=1, stream=False, presence_penalty=0, n=1)` 进行初始化一个大模型，里面是OpenAI需要传入的一些参数，具体可以查看[https://platform.openai.com/docs/api-reference/chat/create](https://platform.openai.com/docs/api-reference/chat/create) 查看具体含义，这里不做详细讲解，如果你不想理会这些参数，你也可以直接`llm = OpenAI()`就好啦，默认使用`gpt-3.5-turbo` 作为大语言模型，其他参数使用默认的就好了。

LLM为`promptulate`
中最基础的组件，为框架提供大语言模型交互能力，如果你想构建更加复杂的大语言模型应用，请跳转[Framework](modules/framework.md#Framework)
和[Agent](modules/agent.md#Agent)。按照顺序阅读`promptulate`官方文档是一个很好的学习方式。

### stop停词
你也许知道使用OpenAI的LLM的时候，可以进行stop(停词)，什么是stop呢？

事实上，stop是一个字符串数组，如`["action", "observation"]`，在LLM生成文本的过程中，如果检测到LLM当前生成本文为stop数组里的内容，则LLM就会停止文本生成，该功能一般用于一些复杂应用程序的开发上，下面的示例展示了stop的使用。

```python
from promptulate.llms import OpenAI

llm = OpenAI(temperature=0)
prompt = """
Please strictly output the following content.
[start] This is a test [end]
"""
result = llm(prompt, stop=["test"])
```

输出结果如下：

```text
[start] This is a
```

llm是否支持stop，要看其LLM模型本身是否支持，当前OpenAI系列的产品支持stop，因此你可以`ChatOpenAI` `OpenAI`都可以使用上面的方式进行调用。

### proxy
我想你可能遇到了无法访问的小问题，It's OK, `promptulate` 提供了三种访问OpenAI的方式，分别是

- `off` 默认的访问方式，不开代理（如果你打开了全局代理工具，可以选择该模式）
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

> 和OPENAI_API_KEY一样，关于代理的配置也设置了缓存，这意味着你只需要配置一次代理即可。事实上`promptulate`
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
    {"model": "gpt-3.5-turbo", "keys": "key1,key2,key3"},
    {"model": "gpt-4", "keys": "xxxxx"},
]

export_openai_key_pool(keys)

llm = OpenAI()
for i in range(10):
    llm("你好")
```

上面的示例中，当你使用了`export_openai_key_pool(keys)`之后，cache会进行缓存，因此在下一次执行的时候，你就无需再导入key或key
pool就可以使用OpenAI进行推理了。

> 如果你想要使用`text-davinci-003`，在key导入的时候你也可以直接用`gpt-3.5-turbo`模型进行导入，而不需要单独声明是`text-davinci-003`模型的key。

需要注意的是，cache会初始化key pool中的数据，因此如果你的一些key失效了，可以尝试重新执行该命令进行初始化操作，或者你可以使用如下删除key_pool中的指定key。

```python
from promptulate.utils.openai_key_pool import OpenAIKey, OpenAIKeyPool

key_pool: OpenAIKeyPool = OpenAIKeyPool()
key_pool.delete("your key")
```

使用下面的方式可以进行查询当前key_pool中的所有key。

```python
from promptulate.utils.openai_key_pool import OpenAIKey, OpenAIKeyPool

key_pool: OpenAIKeyPool = OpenAIKeyPool()
keys = key_pool.all()
for key in keys:
    print(key)
```

输入如下所示：

```text
{'__name__': 'OpenAIKey', '__unique_id__': '62f56487-d528-4f5c-84bb-9c2a3df7354e', 'model': 'gpt-3.5-turbo', 'key': 'key1'}
{'__name__': 'OpenAIKey', '__unique_id__': 'ac3abd29-c62e-458d-b3cc-3f825594910f', 'model': 'gpt-3.5-turbo', 'key': 'key2'}
{'__name__': 'OpenAIKey', '__unique_id__': 'c90ab3c2-e6c0-4a16-a2f9-a298d6290218', 'model': 'gpt-3.5-turbo', 'key': 'key3'}
{'__name__': 'OpenAIKey', '__unique_id__': 'c13b1965-5034-4463-9409-2ad90ba1d260', 'model': 'gpt-3.5-turbo', 'key': 'key4'}

```
