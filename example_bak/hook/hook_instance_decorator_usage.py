import promptulate as pne
from promptulate.hook import Hook
from promptulate.tools import calculator


@Hook.on_agent_create(hook_type="instance")
def handle_agent_create(**kwargs):
    print("math agent component create")


@Hook.on_agent_start(hook_type="instance")
def handle_agent_start(tool, *args, **kwargs):
    prompt = args[0]
    print(f"math agent instance hook start, user prompt: {prompt}, tool: {tool}")


@Hook.on_agent_result(hook_type="instance")
def handle_agent_result(**kwargs):
    result = kwargs["result"]
    print(f"math agent component result: {result}")


def main():
    hooks = [handle_agent_create, handle_agent_start, handle_agent_result]
    agent = pne.ToolAgent(tools=[calculator], hooks=hooks)
    result = agent.run("What is the 5 power of 6?")
    print(result)


if __name__ == "__main__":
    main()
