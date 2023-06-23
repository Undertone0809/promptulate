# LLM

### 简介

本文将会介绍LLM模块的**基本使用方式，API KEY、KEY池、代理的配置方式**。

LLM指大语言模型，当前市面上常见的大语言模型有GPT3.5, GPT4, LLaMa, InstructGPT等大语言模型。`promptulate`可以支持不同类型的大语言模型调用。

当前`promptulate`只重点适配了OpenAI的GPT3.5和GPT4，其他模型适配尚不成熟，正在开发中，因此下面的示例全部以OpenAI模型为例。如果你有想用的LLM或者更好的想法，欢迎提出你的想法。

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

### LLM快速上手

`promptulate`的架构设计可以轻松兼容不同的大语言模型扩展，在`promptulate`中，llm负责最基本的内容生成部分，因此为最基础的组件。

下面的示例展示了如何使用OpenAI进行交互。

```python
from promptulate.llms import OpenAI

llm = OpenAI()
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

对于大语言模型开发者来说，你或许知道OpenAI的GPT API提供了其他参数以便更好地调整GPT的输出特性，下面的示例展示了一个使用GPT4模型自定义参数的OpenAI模型初始化。

```python
from promptulate.llms import OpenAI

llm = OpenAI(model="gpt-4.0", temperature=0.9, top_p=1, stream=False, presence_penalty=0, n=1)
llm("请介绍一下引力波的放射与广义相对论的必然关系")
```

上面的示例中，使用`OpenAI(model="gpt-4.0", temperature=0.9, top_p=1, stream=False, presence_penalty=0, n=1)`
进行初始化一个大模型，里面是OpenAI需要传入的一些参数，具体可以查看[https://platform.openai.com/docs/api-reference/chat/create](https://platform.openai.com/docs/api-reference/chat/create)
查看具体含义，这里不做详细讲解，如果你不想理会这些参数，你也可以直接`llm = OpenAI()`就好啦，默认使用`gpt-3.5-turbo`
作为大语言模型，其他参数使用默认的就好了。

LLM为`promptulate`
中最基础的组件，为框架提供大语言模型交互能力，如果你想构建更加复杂的大语言模型应用，请跳转[Framework](modules/framework.md#Framework)
和[Agent](modules/agent.md#Agent)。按照顺序阅读`promptulate`官方文档是一个很好的学习方式。

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
    {"model": "gpt-4.0", "key": "xxxxx"},
]

export_openai_key_pool(keys)

llm = OpenAI()
for i in range(10):
    llm("你好")
```