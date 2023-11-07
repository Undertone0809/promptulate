from promptulate.llms import ChatOpenAI
from promptulate.schema import AssistantMessage, MessageSet, SystemMessage, UserMessage


def main():
    messages = MessageSet(
        messages=[
            SystemMessage(content="You are a helpful assitant"),
            UserMessage(content="Hello?"),
        ]
    )

    llm = ChatOpenAI()
    answer: AssistantMessage = llm.predict(messages)
    print(answer.content)


main()
