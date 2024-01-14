from promptulate.llms import ErnieBot

llm = ErnieBot(temperature=0.1, model="ernie-bot-turbo")
prompt = """
Please strictly output the following content.
[start] This is a test [end]
"""
result = llm(prompt, stop=["is"])
print(result)
