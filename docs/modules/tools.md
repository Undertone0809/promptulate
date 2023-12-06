# Tool

## 简介

tools模块为LLM提供了调用外部工具扩展的能力，可以说tools是走向智能化的第一步，通过tools来为LLM构建一套感知反馈系统，可以为LLM应用开发提供更多的可能性，当前，Tool只服务于Agent进行搭配使用。本文将会介绍`promptulate`当前支持的外部工具，以及外部工具、工具套件的基本使用方式，最后还会介绍当前正在开发的一些工具套件。

## 支持的工具

当前`promptulate`支持以下工具：

- DuckDuckGo Search: DDG搜索引擎
- Calculator: 计算器
- Shell: 可以执行shell命令（适配windows，mac和linux操作系统）
- LangchainTool: 移植Langchain相关的工具，可以完美兼容引入使用
- HuggingFaceTool: HuggingFace相关的工具，可以完美兼容引入使用
- IotSwitchMqtt: iot工具，可以发送mqtt信息到iot设备
- HumanFeedBackTool: 在适当的时候引入人类反馈
- Arxiv: Arxiv论文检索工具
- Semantic Scholar: Semantic Scholar论文检索工具，可以检索论文、查询论文参考文献、查询引用该论文的文献
- Python REPL: 可以执行python脚本
- FileManager: 可以进行文件读写
- Sleep: 可以进行暂停，以便在agent中控制事件执行的时间间隔，这对有时间控制需求的用户很有帮助


## 在Agent中使用Tool

Tool模块的主要作用就是为Agent提供tool能力支持，详情查看[Agent](modules/agent.md#agent)

## 工具的使用

在大多数情况下，工具用于给Agent使用，而Tool也可以剥离Agent单独进行使用，下面的示例展示了如何使用一个DuckDuckGo进行外部搜索。

```python
from promptulate.tools import DuckDuckGoTool

tool = DuckDuckGoTool()
tool.run("what is promptulate?")
```

在promptulate中，所有tool都可以使用tool.run()的方式进行运行。

此外，相同的导入方式，你还可以导入以下工具：

```python
from promptulate.tools import (
    DuckDuckGoTool,
    DuckDuckGoReferenceTool,
    Calculator,
    ArxivQueryTool,
    ArxivSummaryTool,
    PaperSummaryTool,
    PythonREPLTool,
    SemanticScholarQueryTool,
    SemanticScholarCitationTool,
    SemanticScholarReferenceTool,
    HumanFeedBackTool,
    IotSwitchTool,
    LangchainTool,
    HuggingFaceTool
)
```

所有的工具都继承`Tool`，因此你可以使用`tool.run(prompt)`的方式进行调用。

## Langchain Tool的使用

promptulate兼容langchain所有的tool，并且完美兼容promptulate的hooks系统，下面的示例展示了如何在promptulate中使用langchain tool。

首先，你需要先安装langchain：

```shell
pip install langchain
```

接着，你可以通过如下方式进行调用，下面的示例调用的langchain的DuckDuckGoSearchRun工具。

```python
from langchain.tools import DuckDuckGoSearchRun
from promptulate.tools import LangchainTool
from promptulate.agents import ToolAgent


def example():
    tools = [LangchainTool(DuckDuckGoSearchRun())]
    agent = ToolAgent(tools)
    agent.run("Shanghai weather tomorrow")


if __name__ == "__main__":
    example()
```

## 自定义Tool

promptulate支持自定义tool，其定义方式十分简单，并且提供了函数式和继承式两种方式进行自定义，下面将会展示两种工具定义方式。

### 函数式（推荐）

如果你的tool逻辑较为简单，promptulate提供了方便地函数式工具定义方式，下面的示例展示了一个模拟搜索引擎工具的定义与使用：

```python
from promptulate.tools import define_tool


def web_search(query: str):
    return f"answer: {query}"


def example():
    tool = define_tool(name="web_search", description="A web search tool", callback=web_search)
    tool.run("Shanghai weather tomorrow.")

    
if __name__ == '__main__':
    example()
```

如果你的工具逻辑较为复杂，可以使用继承式的定义方式，下面的示例展示了如何自定义一个Tool类，从而构建一个shell工具。

```python
import warnings
import sys

from promptulate.tools import Tool
from promptulate.tools.shell.api_wrapper import ShellAPIWrapper


def _get_platform() -> str:
    """Get platform."""
    system = sys.platform
    if system == "Darwin":
        return "MacOS"
    return system


class ShellTool(Tool):
    """Tool to run shell commands."""

    name: str = "terminal"
    description: str = f"Run shell commands on this {_get_platform()} machine."
    api_wrapper: ShellAPIWrapper = ShellAPIWrapper()

    def _run(self, command: str) -> str:
        warnings.warn(
            "The shell tool has no safeguards by default. Use at your own risk."
        )
        """Run commands and return final output."""
        return self.api_wrapper.run(command)


def example():
    tool = ShellTool()
    tool.run("echo HelloWorld")

    
if __name__ == '__main__':
    example()
```

上面的示例继承了Tool，并且需要实现name和description两个属性，用于给Agent构建system prompt的输入，此外，你还需要实现_run方法，通过_run来运行tool，对于一个复杂的Tool，你可以采用上面的方式进行定义与逻辑处理。


## 有LLM能力的Tool

在`promptulate`中，为了构建更加智能的Agent，一些提供给Agent的Tool也是有大语言模型调用权限的，它们一般有一些简单的能力处理功能。如果你有需要，你可以直接使用这些带有LLM的Tool，下一章节会演示如何使用Tool。

下面是一些有`LLM能力`的Tools：

- ArxivSummaryTool: Arxiv论文总结工具，可以提供该论文的摘要、关键见解、经验教训、参考文献、相关建议
- PaperSummaryTool: 一个强大的论文总结工具，从Semantic Scholar和Arxiv中检索数据，可以提供该论文的摘要、关键见解、经验教训、参考文献、相关建议
- EnhancedSearchTool: 增强型搜索引擎总结工具，可以同时调用多种搜索引擎进行数据处理。
- IotSwitchMqtt: 可以智能识别输入的自然语言是否符合控制规则表。
- Calculator: 计算器，主要用于准确识别分析用户输入

## 单独使用Tool

如果你想做一些有趣的其他应用，你也可以直接执行该工具。使用`promptulate`执行工具十分简单，对于所有的工具，你都可以使用run()
方法运行。

### 只有基础能力的Tool

下面的示例展示了使用ArxivQueryTool进行Arxiv相关论文的检索。

```python
from promptulate.tools.arxiv import ArxivQueryTool

tool = ArxivQueryTool()
result: str = tool.run("LLM")
print(result)
```

输出如下:

```text
entry_id:http://arxiv.org/abs/2306.05212v1 title:RETA-LLM: A Retrieval-Augmented Large Language Model Toolkit authors:[arxiv.Result.Author('Jiongnan Liu'), arxiv.Result.Author('Jiajie Jin'), arxiv.Result.Author('Zihan Wang'), arxiv.Result.Author('Jiehan Cheng'), arxiv.Result.Author('Zhicheng Dou'), arxiv.Result.Author('Ji-Rong Wen')] summary:Although Large Language Models (LLMs) have demonstrated extraordinary
capabilities in many domains, they still have a tendency to hallucinate and
generate fictitious responses to user requests. This problem can be alleviated
by augmenting LLMs with information retrieval (IR) systems (also known as
retrieval-augmented LLMs). Applying this strategy, LLMs can generate more
factual texts in response to user input according to the relevant content
retrieved by IR systems from external corpora as references. In addition, by
incorporating external knowledge, retrieval-augmented LLMs can answer in-domain
questions that cannot be answered by solely relying on the world knowledge
stored in parameters. To support research in this area and facilitate the
development of retrieval-augmented LLM systems, we develop RETA-LLM, a
{RET}reival-{A}ugmented LLM toolkit. In RETA-LLM, we create a complete pipeline
to help researchers and users build their customized in-domain LLM-based
systems. Compared with previous retrieval-augmented LLM systems, RETA-LLM
provides more plug-and-play modules to support better interaction between IR
systems and LLMs, including {request rewriting, document retrieval, passage
extraction, answer generation, and fact checking} modules. Our toolkit is
publicly available at https://github.com/RUC-GSAI/YuLan-IR/tree/main/RETA-LLM. ;

entry_id:http://arxiv.org/abs/2305.12720v1 title:llm-japanese-dataset v0: Construction of Japanese Chat Dataset for Large Language Models and its Methodology authors:[arxiv.Result.Author('Masanori Hirano'), arxiv.Result.Author('Masahiro Suzuki'), arxiv.Result.Author('Hiroki Sakaji')] summary:This study constructed a Japanese chat dataset for tuning large language
models (LLMs), which consist of about 8.4 million records. Recently, LLMs have
been developed and gaining popularity. However, high-performing LLMs are
usually mainly for English. There are two ways to support languages other than
English by those LLMs: constructing LLMs from scratch or tuning existing
models. However, in both ways, datasets are necessary parts. In this study, we
focused on supporting Japanese in those LLMs and making a dataset for training
or tuning LLMs in Japanese. The dataset we constructed consisted of various
tasks, such as translation and knowledge tasks. In our experiment, we tuned an
existing LLM using our dataset and evaluated the performance qualitatively. The
results suggest that our dataset is possibly beneficial for LLMs. However, we
also revealed some difficulties in constructing LLMs in languages other than
English. ;

entry_id:http://arxiv.org/abs/2305.05176v1 title:FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance authors:[arxiv.Result.Author('Lingjiao Chen'), arxiv.Result.Author('Matei Zaharia'), arxiv.Result.Author('James Zou')] summary:There is a rapidly growing number of large language models (LLMs) that users
can query for a fee. We review the cost associated with querying popular LLM
APIs, e.g. GPT-4, ChatGPT, J1-Jumbo, and find that these models have
heterogeneous pricing structures, with fees that can differ by two orders of
magnitude. In particular, using LLMs on large collections of queries and text
can be expensive. Motivated by this, we outline and discuss three types of
strategies that users can exploit to reduce the inference cost associated with
using LLMs: 1) prompt adaptation, 2) LLM approximation, and 3) LLM cascade. As
an example, we propose FrugalGPT, a simple yet flexible instantiation of LLM
cascade which learns which combinations of LLMs to use for different queries in
order to reduce cost and improve accuracy. Our experiments show that FrugalGPT
can match the performance of the best individual LLM (e.g. GPT-4) with up to
98% cost reduction or improve the accuracy over GPT-4 by 4% with the same cost.
The ideas and findings presented here lay a foundation for using LLMs
sustainably and efficiently. ;

entry_id:http://arxiv.org/abs/2306.08302v2 title:Unifying Large Language Models and Knowledge Graphs: A Roadmap authors:[arxiv.Result.Author('Shirui Pan'), arxiv.Result.Author('Linhao Luo'), arxiv.Result.Author('Yufei Wang'), arxiv.Result.Author('Chen Chen'), arxiv.Result.Author('Jiapu Wang'), arxiv.Result.Author('Xindong Wu')] summary:Large language models (LLMs), such as ChatGPT and GPT4, are making new waves
in the field of natural language processing and artificial intelligence, due to
their emergent ability and generalizability. However, LLMs are black-box
models, which often fall short of capturing and accessing factual knowledge. In
contrast, Knowledge Graphs (KGs), Wikipedia and Huapu for example, are
structured knowledge models that explicitly store rich factual knowledge. KGs
can enhance LLMs by providing external knowledge for inference and
interpretability. Meanwhile, KGs are difficult to construct and evolving by
nature, which challenges the existing methods in KGs to generate new facts and
represent unseen knowledge. Therefore, it is complementary to unify LLMs and
KGs together and simultaneously leverage their advantages. In this article, we
present a forward-looking roadmap for the unification of LLMs and KGs. Our
roadmap consists of three general frameworks, namely, 1) KG-enhanced LLMs,
which incorporate KGs during the pre-training and inference phases of LLMs, or
for the purpose of enhancing understanding of the knowledge learned by LLMs; 2)
LLM-augmented KGs, that leverage LLMs for different KG tasks such as embedding,
completion, construction, graph-to-text generation, and question answering; and
3) Synergized LLMs + KGs, in which LLMs and KGs play equal roles and work in a
mutually beneficial way to enhance both LLMs and KGs for bidirectional
reasoning driven by both data and knowledge. We review and summarize existing
efforts within these three frameworks in our roadmap and pinpoint their future
research directions. ;

entry_id:http://arxiv.org/abs/2303.10130v4 title:GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models authors:[arxiv.Result.Author('Tyna Eloundou'), arxiv.Result.Author('Sam Manning'), arxiv.Result.Author('Pamela Mishkin'), arxiv.Result.Author('Daniel Rock')] summary:We investigate the potential implications of large language models (LLMs),
such as Generative Pre-trained Transformers (GPTs), on the U.S. labor market,
focusing on the increased capabilities arising from LLM-powered software
compared to LLMs on their own. Using a new rubric, we assess occupations based
on their alignment with LLM capabilities, integrating both human expertise and
GPT-4 classifications. Our findings reveal that around 80% of the U.S.
workforce could have at least 10% of their work tasks affected by the
introduction of LLMs, while approximately 19% of workers may see at least 50%
of their tasks impacted. We do not make predictions about the development or
adoption timeline of such LLMs. The projected effects span all wage levels,
with higher-income jobs potentially facing greater exposure to LLM capabilities
and LLM-powered software. Significantly, these impacts are not restricted to
industries with higher recent productivity growth. Our analysis suggests that,
with access to an LLM, about 15% of all worker tasks in the US could be
completed significantly faster at the same level of quality. When incorporating
software and tooling built on top of LLMs, this share increases to between 47
and 56% of all tasks. This finding implies that LLM-powered software will have
a substantial effect on scaling the economic impacts of the underlying models.
We conclude that LLMs such as GPTs exhibit traits of general-purpose
technologies, indicating that they could have considerable economic, social,
and policy implications. ;
```

### 有LLM能力的Tool

接下来我们使用PaperSummaryTool来演示一下给Tool赋能LLM之后的表现，下面的示例展示了使用PaperSummaryTool搜索论文`attention is all you need`

```python
from promptulate.tools.paper.tools import PaperSummaryTool
from promptulate.utils.logger import enable_log

enable_log()


def main():
    tool = PaperSummaryTool()
    result = tool.run("Attention Is All You Need")
    # you can also input an arxiv id as follows
    # result = tool.run("2303.09014")
    print(result)


if __name__ == "__main__":
    main()
```

输出结果如下

```text
标题：注意力就是你所需要的

摘要：目前主流的序列转换模型基于复杂的循环或卷积神经网络，采用编码器-解码器结构。表现最好的模型还通过注意力机制连接编码器和解码器。我们提出了一种新的简单网络架构——Transformer，仅基于注意力机制，完全摒弃了循环和卷积。在两个机器翻译任务上的实验表明，这些模型在质量上优于其他模型，同时更易于并行化，训练时间显著缩短。我们的模型在WMT 2014年英德翻译任务上实现了28.4 BLEU的成绩，超过了现有最佳结果，包括集成模型，提高了2个BLEU。在WMT 2014年英法翻译任务中，我们的模型在8个GPU上训练3.5天后，实现了新的单模型最优BLEU得分41.8，训练成本仅为文献中最佳模型的一小部分。我们证明Transformer在其他任务上具有很好的泛化能力，成功地将其应用于英语成分句法分析，无论是大规模还是有限的训练数据。

关键词：Transformer, attention mechanism, machine translation, BLEU score, parallelizable, training time, generalization.

关键见解：
- 传统的序列转换模型基于复杂的循环或卷积神经网络，而最好的模型通过注意力机制连接编码器和解码器。
- 本文提出了一种新的简单网络架构——Transformer，仅基于注意力机制，完全摒弃了循环和卷积。在机器翻译任务上，这种模型在质量上表现更好，同时更易于并行化，训练时间显著缩短。
- 本文的模型在WMT 2014英德翻译任务上取得了28.4 BLEU的成绩，在WMT 2014英法翻译任务上取得了41.8 BLEU的成绩，成为了单模型下的最佳结果。

经验教训：
- 注意力机制是一种有效的连接编码器和解码器的方式，可以提高序列转换模型的性能。
- 简单的网络架构也可以取得很好的效果，不一定需要复杂的循环或卷积结构。
- Transformer模型具有很好的泛化能力，可以成功应用于其他任务，如英语成分句法分析。

相关建议：
- 进一步探究Transformer网络结构的优化方法，提高其在不同任务上的表现。
- 尝试将Transformer应用于其他自然语言处理任务，如文本分类、命名实体识别等。
- 研究如何在Transformer中引入外部知识，如知识图谱等，以提高其对语义的理解和表达能力。
- 探索如何将Transformer应用于多语言翻译任务，以实现更加高效和准确的跨语言翻译。
- 研究如何在Transformer中引入对抗训练等方法，以提高其对抗攻击的鲁棒性。

相关论文：

[1] [Convolutional Sequence to Sequence Learning](https://www.semanticscholar.org/paper/43428880d75b3a14257c3ee9bda054e61eb869c0)

[2] [Massive Exploration of Neural Machine Translation Architectures](https://www.semanticscholar.org/paper/4550a4c714920ef57d19878e31c9ebae37b049b2)

[3] [A Structured Self-attentive Sentence Embedding](https://www.semanticscholar.org/paper/204a4a70428f3938d2c538a4d74c7ae0416306d8)

[4] [Factorization tricks for LSTM networks](https://www.semanticscholar.org/paper/79baf48bd560060549998d7b61751286de062e2a)

[5] [Structured Attention Networks](https://www.semanticscholar.org/paper/13d9323a8716131911bfda048a40e2cde1a76a46)

[6] [Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer](https://www.semanticscholar.org/paper/510e26733aaff585d65701b9f1be7ca9d5afc586)

[7] [Neural Machine Translation in Linear Time](https://www.semanticscholar.org/paper/98445f4172659ec5e891e031d8202c102135c644)

[8] [Can Active Memory Replace Attention?](https://www.semanticscholar.org/paper/735d547fc75e0772d2a78c46a1cc5fad7da1474c)

[9] [Xception: Deep Learning with Depthwise Separable Convolutions](https://www.semanticscholar.org/paper/5b6ec746d309b165f9f9def873a2375b6fb40f3d)

[10] [Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation](https://www.semanticscholar.org/paper/dbde7dfa6cae81df8ac19ef500c42db96c3d1edd)


```

输出结果已经被排版成markdown格式的数据，因此很适合被渲染出来显示。

此外，上面的例子中，含有多步的LLM推理（四次推理过程）和多次API调用（从Arxiv和Semantic
Scholar中获取论文、引用等相关数据），但是`prompulate`的事件总线并行机制大大化简了推理总时间，平均推理时间保持在十几秒（具体事件取决于网络环境）。

因为采用并行机制，因此在使用有LLM能力的Tool或者Agent时会在同一时间内快速地多次调用API，如果你的key有限速问题，推荐你使用[key-pool](modules/llm/llm.md#key池)来解决key限速的问题（如果你是5美元的key）。
