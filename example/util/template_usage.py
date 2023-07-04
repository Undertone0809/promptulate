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
