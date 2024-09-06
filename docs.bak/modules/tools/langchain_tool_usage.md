# LangChain Tool Usage

Promptulate Agent can use LangChain Tool directly, this document shows how to use the LangChain tool in ToolAgent. 

You can see all LangChain tool [here](https://python.langchain.com/docs/integrations/tools).

## Quick Start

Now, let's see how to use LangChain tool in ToolAgent. The following example, we use LangChain ArXiv tool to get the latest papers from ArXiv.

Before we start, we need to install the LangChain tool package and ArXiv.

```bash
pip install langchain
pip install arxiv
```


```python
import promptulate as pne
from langchain.agents import load_tools

tools: list = load_tools(['arxiv'])
agent = pne.ToolAgent(tools=tools)
agent.run("What's the paper 1605.08386 about?")
```

Output:

```text
Agent Start...
[User] What's the paper 1605.08386 about?
[Thought] I should use the arxiv tool to find information about the paper.
[Action] arxiv args: 1605.08386
[Agent Result] The paper 1605.08386 is titled 'Heat-bath random walks with Markov bases'. It is written by Caprice Stanley and Tobias Windisch. The paper studies graphs on lattice points whose edges come from a finite set of allowed moves. The authors show that the diameter of these graphs can be bounded from above by a constant. They also study the mixing behavior of heat-bath random walks on these graphs and provide conditions for the heat-bath random walk to be an expander in fixed dimension.
```

It's simple, right?

Or you can use the following code to get the same result.


```python
import promptulate as pne

from langchain.tools.arxiv.tool import ArxivQueryRun

# build LangChain tool
arxiv_tool = pne.tools.LangchainTool(ArxivQueryRun())
agent = pne.ToolAgent(tools=[arxiv_tool])
agent.run("What's the paper 1605.08386 about?")
```

## Use DALL-E Image Generator

OpenAI Dall-E are text-to-image models developed by OpenAI using deep learning methodologies to generate digital images from natural language descriptions, called “prompts”. Now you can use DALL-E Image Generator Tool of LangChain to generate images from natural language descriptions.

See [here](https://python.langchain.com/docs/integrations/tools/dalle_image_generator) to get more information about how to get DALL-E Image Generator Tool of LangChain.

The following example, we use DALL-E Image Generator Tool of LangChain to generate an image from a natural language description.


```python
import promptulate as pne
from langchain.agents import load_tools

tools: list = load_tools(["dalle-image-generator"])
agent = pne.ToolAgent(tools=tools)
output = agent.run("Create an image of a halloween night at a haunted museum")
```

output:

```text
Here is the generated image: [![Halloween Night at a Haunted Museum](https://oaidalleapiprodscus.blob.core.windows.net/private/org-OyRC1wqD0EP6oWMS2n4kZgVi/user-JWA0mHqDqYh3oPpQtXbWUPgu/img-SH09tWkWZLJVltxifLi6jFy7.png)]
```

![Halloween Night at a Haunted Museum](../../images/dall-e-gen.png)
