from promptulate.hook import Hook
from promptulate.tools import Calculator


@Hook.on_tool_create(hook_type="instance")
def handle_tool_create(**kwargs):
    print("math tool component create")


@Hook.on_tool_start(hook_type="instance")
def handle_tool_start(*args, **kwargs):
    prompt = args[0]
    print(f"math tool instance hook start, user prompt: {prompt}")


@Hook.on_tool_result(hook_type="instance")
def handle_tool_result(**kwargs):
    result = kwargs["result"]
    print(f"math tool component result: {result}")


def main():
    hooks = [handle_tool_create, handle_tool_start, handle_tool_result]
    tool = Calculator(hooks=hooks)
    result = tool.run("6的五次方等于多少")
    print(result)


if __name__ == "__main__":
    main()
