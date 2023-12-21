# String Template

String Template是`promptulate`用于格式化prompt的工具，其功能很简单，就是字符串格式化。

下面的示例展示了如何构建一个ReAct的prompt：

```python
from promptulate.utils import StringTemplate

prompt = """
Answer the following questions as best you can. You have access to the following tools:
{tool_description}
Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_name}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {question}
Thought:
"""

tool_description = """
duckduckgo_search: A wrapper around DuckDuckGo Search. Useful for when you need to answer questions about current events. Input should be a search query.

Calculator: Useful for when you need to answer questions about math.
"""

tool_name = """duckduckgo_search, Calculator"""

question = "Tell me a funny joke about chickens."
string_template = StringTemplate(prompt)
prompt = string_template.format([tool_description, tool_name, question])
print(prompt)

```

上面的示例中，format传入数组，那么这个数组就需要按照字符串模板中的变量顺序来进行传参。

当然，你也可以使用如下方式进行format，也是同理：

```python
string_template.format(tool_name=tool_name, tool_description=tool_description, question=question)
```

输入如下：

```text
Answer the following questions as best you can. You have access to the following tools:

duckduckgo_search: A wrapper around DuckDuckGo Search. Useful for when you need to answer questions about current events. Input should be a search query.

Calculator: Useful for when you need to answer questions about math.

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [duckduckgo_search, Calculator]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: Tell me a funny joke about chickens.
Thought:
```

## Jinja2
In some cases, you will get error when you use single curly braces. For example, the following code will raise an error.

```python
from promptulate.utils import StringTemplate

data = "test"
prompt = "This is a {data} {'key': 'value'}"

resp: str = StringTemplate(prompt).format(data=data)
print(resp)
```

Output:

```text
Traceback (most recent call last):
  File "/Users/xxx/PycharmProjects/promptulate/venv/lib/python3.8/site-packages/promptulate/utils/string_template.py", line 31, in format
    return self.template.format(*args, **kwargs)
KeyError: "'key'"
```

StringTemplate use f-string default, it will get error when facing `{'key':'value'}`. The follow example show how to use Jinja2 to avoid this error.

```python
from promptulate.utils import StringTemplate

data = "test"
prompt = """This is a {{data}} {'key': 'value'}"""

resp: str = StringTemplate(prompt, template_format="jinja2").format(data=data)
print(resp)
```

Output:

```text
This is a test {'key': 'value'}
```

**Therefore, you can use `{{variable}}` to avoid some potential problems by jinja2.**