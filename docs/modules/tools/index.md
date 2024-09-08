# Tool

The tools module provides LLM with the ability to extend external tools, which can be said to be the first step towards intelligence. Through tools, a perception feedback system can be built for LLM, providing more possibilities for LLM application development. Currently, Tool only serves Agent for pairing use. This article will introduce the external tools currently supported by `promptulate`, as well as the basic usage of external tools and toolkits, and finally introduce some toolkits that are currently under development.

## Supported Tools

Currently, `promptulate` has integrated the following tools:

- DuckDuckGo Search: DDG search engine
- Calculator: calculator
- Shell: can execute shell commands (compatible with Windows, Mac, and Linux operating systems)
- LangchainTool: ported Langchain-related tools, can be perfectly compatible for use
- HuggingFaceTool: HuggingFace-related tools, can be perfectly compatible for use
- IotSwitchMqtt: iot tool, can send mqtt messages to iot devices
- HumanFeedBackTool: introduces human feedback at appropriate times
- Arxiv: Arxiv paper search tool
- Semantic Scholar: Semantic Scholar paper search tool, can search papers, query paper references, and query papers citing this paper
- Python REPL: can execute python scripts
- FileManager: can perform file read and write operations
- Sleep: can pause, which is very helpful for users who need time control in the agent to control the time interval of event execution

## Using Tool in Agent

The primary function of the Tool module is to provide tool capability support for Agent, see details in [Agent](/modules/agent.md#agent).

## Custom Tool

See details in [Custom Tool](/modules/tools/custom_tool_usage.md#custom-tool).

## Tool Usage

In most cases, tools are used for Agent usage, and Tool can also be separated from Agent for standalone use. The following example demonstrates how to use a DuckDuckGo for external search.

```python
from promptulate.tools import DuckDuckGoTool

tool = DuckDuckGoTool()
tool.run("what is promptulate?")
```

In promptulate, all tools can be run using the tool.run() method.

Additionally, with the same import method, you can also import the following tools:

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

All tools inherit from `Tool`, so you can use the `tool.run(prompt)` method to call them.

## Using LangChain Tool

Promptulate is compatible with all LangChain tools and perfectly compatible with Promptulate's hooks system. See the details in [LangChain Tool usage](/modules/tools/langchain_tool_usage.md)

## Tools with LLM Capabilities

In Promptulate, some tools provided to the Agent also have the ability to call large language models, which generally have some simple capability processing functions. If you need to, you can directly use these tools with LLM capabilities, and the next section will demonstrate how to use them.

Here are some tools with LLM capabilities:

- ArxivSummaryTool: Arxiv paper summary tool, can provide the paper's summary, key insights, lessons learned, references, and related suggestions
- PaperSummaryTool: A powerful paper summary tool, retrieves data from Semantic Scholar and Arxiv, can provide the paper's summary, key insights, lessons learned, references, and related suggestions
- EnhancedSearchTool: Enhanced search engine summary tool, can call multiple search engines for data processing at the same time.
- IotSwitchMqtt: Can intelligently recognize whether the input natural language conforms to the control rule table.
- Calculator: Calculator, mainly used for accurate recognition and analysis of user input

## Using Tool Independently

If you want to do some other interesting applications, you can also execute the tool directly. Using Promptulate to execute tools is very simple, and for all tools, you can use the `run()` method to run them.

### Basic Capability Tools

The following example demonstrates using ArxivQueryTool to search for Arxiv-related papers.

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

### Tool with LLM Capability

Next, we will demonstrate the performance of a Tool after being empowered with LLM using the PaperSummaryTool. The following example shows the result of searching for the paper "Attention Is All You Need" using the PaperSummaryTool:

```python
from promptulate.tools.paper.tools import PaperSummaryTool


def main():
    tool = PaperSummaryTool()
    result = tool.run("Attention Is All You Need")
    # you can also input an arxiv id as follows
    # result = tool.run("2303.09014")
    print(result)


if __name__ == "__main__":
    main()
```

The output result is as follows

```text
Title: Attention Is All You Need

Summary: The current mainstream sequence transformation models are based on complex recurrent or convolutional neural networks, adopting an encoder-decoder structure. The best-performing models also use attention mechanisms to connect the encoder and decoder. We propose a new simple network architecture—the Transformer, which is solely based on attention mechanisms, completely discarding recurrence and convolution. Experiments on two machine translation tasks demonstrate that these models outperform other models in quality, while being easier to parallelize, significantly reducing training time. Our model achieves a score of 28.4 BLEU on the WMT 2014 English-to-German translation task, surpassing the current best result, including ensemble models, by 2 BLEU points. On the WMT 2014 English-to-French translation task, our model achieves a new single-model best BLEU score of 41.8 after training for 3.5 days on 8 GPUs, with training costs being only a fraction of the best model in the literature. We prove that the Transformer has good generalization capabilities, successfully applying it to English constituent parsing, regardless of the scale or limitation of the training data.

Keywords: Transformer, attention mechanism, machine translation, BLEU score, parallelizable, training time, generalization.

Key Insights:
- Traditional sequence transformation models are based on complex recurrent or convolutional neural networks, while the best models use attention mechanisms to connect the encoder and decoder.
- This paper proposes a new simple network architecture—the Transformer, which is solely based on attention mechanisms, completely discarding recurrence and convolution. On machine translation tasks, this model performs better in quality, while being easier to parallelize, significantly reducing training time.
- This paper's model achieves a score of 28.4 BLEU on the WMT 2014 English-to-German translation task and a score of 41.8 BLEU on the WMT 2014 English-to-French translation task, becoming the best single-model result.

Lessons Learned:
- Attention mechanisms are an effective way to connect the encoder and decoder, which can improve the performance of sequence transformation models.
- Simple network architectures can also achieve good results, not necessarily requiring complex recurrent or convolutional structures.
- The Transformer model has good generalization capabilities, successfully applying it to other tasks, such as English constituent parsing.

Recommendations:
- Further explore the optimization methods of the Transformer network structure to improve its performance on different tasks.
- Attempt to apply the Transformer to other natural language processing tasks, such as text classification, named entity recognition, etc.
- Research how to introduce external knowledge, such as knowledge graphs, into the Transformer to improve its understanding and expression of semantics.
- Explore how to apply the Transformer to multilingual translation tasks to achieve more efficient and accurate cross-language translation.
- Research how to introduce adversarial training methods into the Transformer to improve its robustness against adversarial attacks.

Related Papers:

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

The output result is formatted in markdown format, making it suitable for rendering and display.

Furthermore, the example above involves multiple steps of LLM inference (four inference processes) and multiple API calls (retrieving paper and citation data from Arxiv and Semantic Scholar), but the event bus parallel mechanism of `prompulate` greatly simplifies the total inference time, maintaining an average inference time of around ten seconds (specific events depend on the network environment).

Due to the use of parallel mechanisms, when using a Tool or Agent with LLM capabilities, you will rapidly make multiple API calls simultaneously. If you encounter rate limit issues with your key, we recommend using the [key-pool](/modules/llm/llm.md#key-pool) to solve key rate limit problems (if you have a $5 key).
