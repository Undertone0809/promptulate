# tools

文档完善中...

## 简介

tools模块为LLM提供了调用外部工具扩展的能力，可以说tools是走向智能化的第一步，通过tools来为LLM构建一套感知反馈系统，可以为LLM应用开发提供更多的可能性。本文将会介绍`promptulate`
当前支持的外部工具，以及外部工具、工具套件的基本使用方式，最后还会介绍当前正在开发的一些工具套件。

## 支持的工具

当前`promptulate`支持以下几种工具：

- DuckDuckGo Search: DDG搜索引擎
- Arxiv: Arxiv论文检索工具
- Semantic Scholar: Semantic Scholar论文检索工具，可以检索论文、查询论文参考文献、查询引用该论文的文献
- Python REPL: 可以执行python脚本
- FileManager: 可以进行文件读写
- ...

## 有LLM能力的Tool

在`promptulate`
中，为了构建更加智能的Agent，一些提供给Agent的Tool也是有大语言模型调用权限的，它们一般有一些简单的能力处理功能。如果你有需要，你可以直接使用这些带有LLM的Tool，下一章节会演示如何使用Tool。

下面是一些有`LLM能力`的Tools：
- ArxivSummaryTool: Arxiv论文总结工具，可以提供该论文的摘要、关键见解、经验教训、参考文献、相关建议
- PaperSummaryTool: 一个强大的论文总结工具，从Semantic Scholar和Arxiv中检索数据，可以提供该论文的摘要、关键见解、经验教训、参考文献、相关建议
- EnhancedSearchTool: 增强型搜索引擎总结工具，可以同时调用多种搜索引擎进行数据处理。

## 单独使用Tool

如果你想做一些有趣的其他应用，你也可以直接执行该工具。使用`promptulate`执行工具十分简单，对于所有的工具，你都可以使用run()
方法运行。

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

## 在Agent中使用Tool

待完善...