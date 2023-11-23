from promptulate.utils.string_template import StringTemplate

SYSTEM_PROMPT = """
Answer the following questions as best you can. You have access use web search.
After the user enters a question, you need to generate keywords for web search,
and then summarize until you think you can answer the user's answer.

Your output format is as follows:
Question: the input question you must answer
Thought: The next you should do
Query: web search query words
Observation: the result of query
... (this Thought/Query/Observation can repeat N times)
Thought: I know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {prompt}

Thought:"""

SYSTEM_PROMPT_TEMPLATE = StringTemplate(SYSTEM_PROMPT)
