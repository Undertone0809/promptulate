"""This example will show how to use a specified key in OpenAI model."""
from promptulate.llms import ChatOpenAI


def main():
    llm = ChatOpenAI()
    llm.set_private_api_key("your key here")
    print(llm("hello"))


if __name__ == "__main__":
    main()
