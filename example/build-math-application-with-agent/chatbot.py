import promptulate as pne
from promptulate.llms import ChatOpenAI
from promptulate.schema import AssistantMessage, MessageSet, SystemMessage, UserMessage
from promptulate.tools.math.tools import calculator
from promptulate.tools.wikipedia.tools import wikipedia_search

llm = ChatOpenAI()

WORD_PROBLEM_TEMPLATE = """You are a reasoning agent tasked with solving t he user's logic-based questions. 
                                Logically arrive at the solution, and be factual. 
                                In your answers, clearly detail the steps involved and give the final answer. 
                                Provide the response in bullet points. Question  {question} Answer"""
user_question = input("Enter your question: ")
formatted_template = WORD_PROBLEM_TEMPLATE.format(question=user_question)

# prompt for reasoning based tool
messages = MessageSet(
    messages=[
        SystemMessage(content=formatted_template),
        UserMessage(content=user_question)
    ]
)


# reasoning based tool
def word_problem_tool():
    """
        description:
        Useful for when you need to answer logic-based/reasoning questions.
    """
    response: AssistantMessage = llm.predict(messages)
    return response


# calculator tool for arithmetics
def math_tool(expression):
    """
        description:
            Useful for when you need to answer numeric questions.
            Your input is a nature language of math expression. Attention: Expressions can not exist variables!
            eg: (current age)^0.43 is wrong, you should use 18^0.43 instead.
    """
    return calculator(expression)


# Wikipedia Tool
def wikipedia_tool(keyword: str) -> str:
    """search by keyword in web.
        description:
            A useful tool for searching the Internet to find information on world events, issues, dates,years, etc.
            Worth using for general topics. Use precise questions.

        Args:
            keyword: keyword to search

        Returns:
            str: search result
        """
    return wikipedia_search(keyword)


# 使用自定义Tool的agent
agent = pne.ToolAgent(tools=[wikipedia_tool, math_tool, word_problem_tool],
                      llm=llm)

# 使用内置Tool的agent
# agent = pne.ToolAgent(tools=[wikipedia_search, calculator, word_problem_tool],
#                       llm=llm)

resp: str = agent.run(user_question)
print(resp)
