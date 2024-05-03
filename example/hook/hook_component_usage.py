import promptulate as pne
from promptulate import ChatOpenAI
from promptulate.hook import Hook
from promptulate.tools import calculator
from promptulate.tools.wikipedia import wikipedia_search


@Hook.on_tool_create(hook_type="component")
def handle_tool_create_by_component(*args, **kwargs):
    print("tool component create by component")


def main():
    # handle tool create by component
    llm = ChatOpenAI(model="gpt-4-1106-preview")
    agent = pne.ToolAgent(tools=[wikipedia_search, calculator],
                          llm=llm)
    response: str = agent.run("Tell me the year in which Tom Cruise's Top Gun was "
                              "released, and calculate the square of that year.")
    print(response)


if __name__ == "__main__":
    main()
