# Agent

Agent是`promptulate`的核心组件之一，其核心思想是使用llm、Tool、Memory、Provider,Output Parser等组件来构建起的一个可以处理复杂能力的代理。

下面的示例展示了如何使用`ToolAgent`结合Tool进行使用。

```python
from promptulate.utils.logger import enable_log
from promptulate.tools import (
    DuckDuckGoTool,
    Calculator,
)
from promptulate.agents import ToolAgent

enable_log()


def main():
    tools = [
        DuckDuckGoTool(),
        Calculator(),
    ]
    agent = ToolAgent(tools)
    prompt = """Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"""
    agent.run(prompt)


if __name__ == "__main__":
    main()

```

运行结果如下（开启了debug，便于观察过程的输出结果，后续将会构建PrintHook进行过程输出）：

```text
E:\Programming\anaconda\envs\prompt-me\python.exe D:\Programming\Python\Project\promptulate\example\agent\tool_agent_usage.py 
[INFO] 2023-08-08 02:41:11 [pne] tool agent system prompt: 
Answer the following questions as best you can. You have access to the following tools:

ddg-search: A wrapper around DuckDuckgo Web Search. Useful for when you need to answer questions about current events. Input should be a search query.

math-calculator: Useful for when you need to answer questions about math.You input is a naturelanguage of math expression.


Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, must be one of [ddg-search, math-calculator]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?
Thought:

[DEBUG] 2023-08-08 02:41:11 [pne openai params] body {"messages": [{"role": "system", "content": ""}, {"role": "user", "content": "\nAnswer the following questions as best you can. You have access to the following tools:\n\nddg-search: A wrapper around DuckDuckgo Web Search. Useful for when you need to answer questions about current events. Input should be a search query.\n\nmath-calculator: Useful for when you need to answer questions about math.You input is a naturelanguage of math expression.\n\n\nUse the following format:\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, must be one of [ddg-search, math-calculator]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?\nThought:\n"}], "stop": ["Observation"], "model": "gpt-3.5-turbo-16k", "temperature": 0.2, "top_p": 1, "stream": false, "frequency_penalty": 0, "presence_penalty": 0, "n": 1, "max_tokens": 3000}
[DEBUG] 2023-08-08 02:41:11 [pne openai request] url: https://api.openai.com/v1/chat/completions proxies: {'http': 'http://127.0.0.1:7890'}
[DEBUG] 2023-08-08 02:41:11 Starting new HTTPS connection (1): api.openai.com:443
[DEBUG] 2023-08-08 02:41:14 https://api.openai.com:443 "POST /v1/chat/completions HTTP/1.1" 200 None
[DEBUG] 2023-08-08 02:41:14 [pne openai response] {"id": "chatcmpl-7kzSCQ1V0BuAI30VDz82GO8tOsajl", "object": "chat.completion", "created": 1691433672, "model": "gpt-3.5-turbo-16k-0613", "choices": [{"index": 0, "message": {"role": "assistant", "content": "I need to find out who Leo DiCaprio's girlfriend is and then calculate her current age raised to the 0.43 power. I can use ddg-search to find out who his girlfriend is and then use math-calculator to calculate the power.\n\nAction: ddg-search\nAction Input: \"Leo DiCaprio's girlfriend\"\n"}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 216, "completion_tokens": 69, "total_tokens": 285}}
[DEBUG] 2023-08-08 02:41:14 [pne openai answer] I need to find out who Leo DiCaprio's girlfriend is and then calculate her current age raised to the 0.43 power. I can use ddg-search to find out who his girlfriend is and then use math-calculator to calculate the power.

Action: ddg-search
Action Input: "Leo DiCaprio's girlfriend"

[INFO] 2023-08-08 02:41:14 [pne] tool agent <1> current prompt: 
Answer the following questions as best you can. You have access to the following tools:

ddg-search: A wrapper around DuckDuckgo Web Search. Useful for when you need to answer questions about current events. Input should be a search query.

math-calculator: Useful for when you need to answer questions about math.You input is a naturelanguage of math expression.


Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, must be one of [ddg-search, math-calculator]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?
Thought:
I need to find out who Leo DiCaprio's girlfriend is and then calculate her current age raised to the 0.43 power. I can use ddg-search to find out who his girlfriend is and then use math-calculator to calculate the power.

Action: ddg-search
Action Input: "Leo DiCaprio's girlfriend"


[INFO] 2023-08-08 02:41:14 [pne] tool agent get Action <ddg-search>
[INFO] 2023-08-08 02:41:14 [pne] tool agent get Action Input <"Leo DiCaprio's girlfriend">
[DEBUG] 2023-08-08 02:41:16 [pne tool result] 37-year-old Leo and 23-year-old Erin dated for almost a year, and the split was drama-free. E! News actually asked Erin about it at an event and she said, "I having the best time right now, here ... Leonardo DiCaprio's rumoured new girlfriend is a 22-year-old Ukrainian model named Maria Beregova. The Wolf Of Wall Street actor recently split up with Camila Morrone, 25, who he dated for four ... 15 Stunning Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone / Dating Apps / By admin It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio discovered real love with Camila Morrone? Only time will inform, but as of today things are going strong and they are nonetheless collectively. 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Post author: Goldbic; Post published: May 30, 2023; Post category: Hookup; It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio found true love with Camila Morrone? Only time will inform, but as of right now things are going ... 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Best Dating Site / Por admin. It was like I had outgrown that version of myself, the Hollywood highschool lady. Has Leonardo Dicaprio discovered true love with Camila Morrone? Only time will inform, however as of at present issues are going robust and they are nonetheless ...
[DEBUG] 2023-08-08 02:41:16 [pne openai params] body {"messages": [{"role": "system", "content": ""}, {"role": "user", "content": "\nAnswer the following questions as best you can. You have access to the following tools:\n\nddg-search: A wrapper around DuckDuckgo Web Search. Useful for when you need to answer questions about current events. Input should be a search query.\n\nmath-calculator: Useful for when you need to answer questions about math.You input is a naturelanguage of math expression.\n\n\nUse the following format:\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, must be one of [ddg-search, math-calculator]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?\nThought:\nI need to find out who Leo DiCaprio's girlfriend is and then calculate her current age raised to the 0.43 power. I can use ddg-search to find out who his girlfriend is and then use math-calculator to calculate the power.\n\nAction: ddg-search\nAction Input: \"Leo DiCaprio's girlfriend\"\n\nObservation: 37-year-old Leo and 23-year-old Erin dated for almost a year, and the split was drama-free. E! News actually asked Erin about it at an event and she said, \"I having the best time right now, here ... Leonardo DiCaprio's rumoured new girlfriend is a 22-year-old Ukrainian model named Maria Beregova. The Wolf Of Wall Street actor recently split up with Camila Morrone, 25, who he dated for four ... 15 Stunning Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone / Dating Apps / By admin It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio discovered real love with Camila Morrone? Only time will inform, but as of today things are going strong and they are nonetheless collectively. 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Post author: Goldbic; Post published: May 30, 2023; Post category: Hookup; It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio found true love with Camila Morrone? Only time will inform, but as of right now things are going ... 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Best Dating Site / Por admin. It was like I had outgrown that version of myself, the Hollywood highschool lady. Has Leonardo Dicaprio discovered true love with Camila Morrone? Only time will inform, however as of at present issues are going robust and they are nonetheless ..."}], "stop": ["Observation"], "model": "gpt-3.5-turbo-16k", "temperature": 0.2, "top_p": 1, "stream": false, "frequency_penalty": 0, "presence_penalty": 0, "n": 1, "max_tokens": 3000}
[DEBUG] 2023-08-08 02:41:16 [pne openai request] url: https://api.openai.com/v1/chat/completions proxies: {'http': 'http://127.0.0.1:7890'}
[DEBUG] 2023-08-08 02:41:16 Starting new HTTPS connection (1): api.openai.com:443
[DEBUG] 2023-08-08 02:41:19 https://api.openai.com:443 "POST /v1/chat/completions HTTP/1.1" 200 None
[DEBUG] 2023-08-08 02:41:19 [pne openai response] {"id": "chatcmpl-7kzSH4N5DSdBvOuWVLG9UEqj28H4I", "object": "chat.completion", "created": 1691433677, "model": "gpt-3.5-turbo-16k-0613", "choices": [{"index": 0, "message": {"role": "assistant", "content": "Thought:\nI found out that Leo DiCaprio's girlfriend is Camila Morrone. Now I need to calculate her current age raised to the 0.43 power. I can use math-calculator for this.\n\nAction: math-calculator\nAction Input: \"23^0.43\"\n\n"}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 622, "completion_tokens": 60, "total_tokens": 682}}
[DEBUG] 2023-08-08 02:41:19 [pne openai answer] Thought:
I found out that Leo DiCaprio's girlfriend is Camila Morrone. Now I need to calculate her current age raised to the 0.43 power. I can use math-calculator for this.

Action: math-calculator
Action Input: "23^0.43"


[INFO] 2023-08-08 02:41:19 [pne] tool agent <2> current prompt: 
Answer the following questions as best you can. You have access to the following tools:

ddg-search: A wrapper around DuckDuckgo Web Search. Useful for when you need to answer questions about current events. Input should be a search query.

math-calculator: Useful for when you need to answer questions about math.You input is a naturelanguage of math expression.


Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, must be one of [ddg-search, math-calculator]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?
Thought:
I need to find out who Leo DiCaprio's girlfriend is and then calculate her current age raised to the 0.43 power. I can use ddg-search to find out who his girlfriend is and then use math-calculator to calculate the power.

Action: ddg-search
Action Input: "Leo DiCaprio's girlfriend"

Observation: 37-year-old Leo and 23-year-old Erin dated for almost a year, and the split was drama-free. E! News actually asked Erin about it at an event and she said, "I having the best time right now, here ... Leonardo DiCaprio's rumoured new girlfriend is a 22-year-old Ukrainian model named Maria Beregova. The Wolf Of Wall Street actor recently split up with Camila Morrone, 25, who he dated for four ... 15 Stunning Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone / Dating Apps / By admin It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio discovered real love with Camila Morrone? Only time will inform, but as of today things are going strong and they are nonetheless collectively. 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Post author: Goldbic; Post published: May 30, 2023; Post category: Hookup; It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio found true love with Camila Morrone? Only time will inform, but as of right now things are going ... 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Best Dating Site / Por admin. It was like I had outgrown that version of myself, the Hollywood highschool lady. Has Leonardo Dicaprio discovered true love with Camila Morrone? Only time will inform, however as of at present issues are going robust and they are nonetheless ...Thought:
I found out that Leo DiCaprio's girlfriend is Camila Morrone. Now I need to calculate her current age raised to the 0.43 power. I can use math-calculator for this.

Action: math-calculator
Action Input: "23^0.43"



[INFO] 2023-08-08 02:41:19 [pne] tool agent get Action <math-calculator>
[INFO] 2023-08-08 02:41:19 [pne] tool agent get Action Input <"23^0.43">
[DEBUG] 2023-08-08 02:41:19 [pne openai params] body {"messages": [{"role": "system", "content": ""}, {"role": "user", "content": "Translate a math problem into a expression that can be executed using Python's numexpr library. Use the output of running this code to answer the question.\n\nQuestion: ${Question with math problem.}\n```text\n${single line mathematical expression that solves the problem}\n```\n...numexpr.evaluate(text)...\n```output\n${Output of running the code}\n```\nAnswer: ${Answer}\n\nBegin.\n\nQuestion: What is 37593 * 67?\n```text\n37593 * 67\n```\n...numexpr.evaluate(\"37593 * 67\")...\n```output\n2518731\n```\nAnswer: 2518731\n\nQuestion: 37593^(1/5)\n```text\n37593**(1/5)\n```\n...numexpr.evaluate(\"37593**(1/5)\")...\n```output\n8.222831614237718\n```\nAnswer: 8.222831614237718\n\nQuestion: \"23^0.43\"\n"}], "stop": ["```output"], "model": "gpt-3.5-turbo", "temperature": 0.0, "top_p": 1, "stream": false, "frequency_penalty": 0, "presence_penalty": 0, "n": 1, "max_tokens": 3000}
[DEBUG] 2023-08-08 02:41:19 [pne openai request] url: https://api.openai.com/v1/chat/completions proxies: {'http': 'http://127.0.0.1:7890'}
[DEBUG] 2023-08-08 02:41:19 Starting new HTTPS connection (1): api.openai.com:443
[DEBUG] 2023-08-08 02:41:21 https://api.openai.com:443 "POST /v1/chat/completions HTTP/1.1" 200 None
[DEBUG] 2023-08-08 02:41:21 [pne openai response] {"id": "chatcmpl-7kzSJdzDuzJle1az1LbdKH1NXoHMW", "object": "chat.completion", "created": 1691433679, "model": "gpt-3.5-turbo-0613", "choices": [{"index": 0, "message": {"role": "assistant", "content": "```text\n23**0.43\n```\n...numexpr.evaluate(\"23**0.43\")...\n"}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 209, "completion_tokens": 23, "total_tokens": 232}}
[DEBUG] 2023-08-08 02:41:21 [pne openai answer] ```text
23**0.43
``
...numexpr.evaluate("23**0.43")...

[DEBUG] 2023-08-08 02:41:22 [pne tool result] 3.8507291225496925
[DEBUG] 2023-08-08 02:41:22 [pne openai params] body {"messages": [{"role": "system", "content": ""}, {"role": "user", "content": "\nAnswer the following questions as best you can. You have access to the following tools:\n\nddg-search: A wrapper around DuckDuckgo Web Search. Useful for when you need to answer questions about current events. Input should be a search query.\n\nmath-calculator: Useful for when you need to answer questions about math.You input is a naturelanguage of math expression.\n\n\nUse the following format:\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, must be one of [ddg-search, math-calculator]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?\nThought:\nI need to find out who Leo DiCaprio's girlfriend is and then calculate her current age raised to the 0.43 power. I can use ddg-search to find out who his girlfriend is and then use math-calculator to calculate the power.\n\nAction: ddg-search\nAction Input: \"Leo DiCaprio's girlfriend\"\n\nObservation: 37-year-old Leo and 23-year-old Erin dated for almost a year, and the split was drama-free. E! News actually asked Erin about it at an event and she said, \"I having the best time right now, here ... Leonardo DiCaprio's rumoured new girlfriend is a 22-year-old Ukrainian model named Maria Beregova. The Wolf Of Wall Street actor recently split up with Camila Morrone, 25, who he dated for four ... 15 Stunning Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone / Dating Apps / By admin It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio discovered real love with Camila Morrone? Only time will inform, but as of today things are going strong and they are nonetheless collectively. 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Post author: Goldbic; Post published: May 30, 2023; Post category: Hookup; It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio found true love with Camila Morrone? Only time will inform, but as of right now things are going ... 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Best Dating Site / Por admin. It was like I had outgrown that version of myself, the Hollywood highschool lady. Has Leonardo Dicaprio discovered true love with Camila Morrone? Only time will inform, however as of at present issues are going robust and they are nonetheless ...Thought:\nI found out that Leo DiCaprio's girlfriend is Camila Morrone. Now I need to calculate her current age raised to the 0.43 power. I can use math-calculator for this.\n\nAction: math-calculator\nAction Input: \"23^0.43\"\n\n\nObservation: 3.8507291225496925"}], "stop": ["Observation"], "model": "gpt-3.5-turbo-16k", "temperature": 0.2, "top_p": 1, "stream": false, "frequency_penalty": 0, "presence_penalty": 0, "n": 1, "max_tokens": 3000}
[DEBUG] 2023-08-08 02:41:22 [pne openai request] url: https://api.openai.com/v1/chat/completions proxies: {'http': 'http://127.0.0.1:7890'}
[DEBUG] 2023-08-08 02:41:22 Starting new HTTPS connection (1): api.openai.com:443
[DEBUG] 2023-08-08 02:41:24 https://api.openai.com:443 "POST /v1/chat/completions HTTP/1.1" 200 None
[DEBUG] 2023-08-08 02:41:24 [pne openai response] {"id": "chatcmpl-7kzSMJKHXqKlZXYXPwsQNDo0U8QFP", "object": "chat.completion", "created": 1691433682, "model": "gpt-3.5-turbo-16k-0613", "choices": [{"index": 0, "message": {"role": "assistant", "content": "Thought: I now know the final answer\nFinal Answer: Camila Morrone's current age raised to the 0.43 power is approximately 3.8507."}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 694, "completion_tokens": 35, "total_tokens": 729}}
[DEBUG] 2023-08-08 02:41:24 [pne openai answer] Thought: I now know the final answer
Final Answer: Camila Morrone's current age raised to the 0.43 power is approximately 3.8507.
[INFO] 2023-08-08 02:41:24 [pne] tool agent <3> current prompt: 
Answer the following questions as best you can. You have access to the following tools:

ddg-search: A wrapper around DuckDuckgo Web Search. Useful for when you need to answer questions about current events. Input should be a search query.

math-calculator: Useful for when you need to answer questions about math.You input is a naturelanguage of math expression.


Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, must be one of [ddg-search, math-calculator]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?
Thought:
I need to find out who Leo DiCaprio's girlfriend is and then calculate her current age raised to the 0.43 power. I can use ddg-search to find out who his girlfriend is and then use math-calculator to calculate the power.

Action: ddg-search
Action Input: "Leo DiCaprio's girlfriend"

Observation: 37-year-old Leo and 23-year-old Erin dated for almost a year, and the split was drama-free. E! News actually asked Erin about it at an event and she said, "I having the best time right now, here ... Leonardo DiCaprio's rumoured new girlfriend is a 22-year-old Ukrainian model named Maria Beregova. The Wolf Of Wall Street actor recently split up with Camila Morrone, 25, who he dated for four ... 15 Stunning Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone / Dating Apps / By admin It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio discovered real love with Camila Morrone? Only time will inform, but as of today things are going strong and they are nonetheless collectively. 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Post author: Goldbic; Post published: May 30, 2023; Post category: Hookup; It was like I had outgrown that model of myself, the Hollywood high school girl. Has Leonardo Dicaprio found true love with Camila Morrone? Only time will inform, but as of right now things are going ... 15 Gorgeous Photographs Of Leo Dicaprio's Girlfriend, Camila Morrone. Best Dating Site / Por admin. It was like I had outgrown that version of myself, the Hollywood highschool lady. Has Leonardo Dicaprio discovered true love with Camila Morrone? Only time will inform, however as of at present issues are going robust and they are nonetheless ...Thought:
I found out that Leo DiCaprio's girlfriend is Camila Morrone. Now I need to calculate her current age raised to the 0.43 power. I can use math-calculator for this.

Action: math-calculator
Action Input: "23^0.43"


Observation: 3.8507291225496925Thought: I now know the final answer
Final Answer: Camila Morrone's current age raised to the 0.43 power is approximately 3.8507.
```