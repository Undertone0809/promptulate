import promptulate as pne
from promptulate.schema import AssistantMessage, MessageSet, SystemMessage, UserMessage

messages = MessageSet(
    messages=[
        SystemMessage(content="You are a helpful assitant"),
        UserMessage(content="Hello?"),
    ]
)

llm = pne.ChatOpenAI()
answer: AssistantMessage = llm.predict(messages)
print(answer.content)
print(answer.additional_kwargs)
