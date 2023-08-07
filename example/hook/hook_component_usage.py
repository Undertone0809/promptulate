# todo agent + tool component hook usage
from promptulate.hook import Hook
from promptulate.tools import Calculator


@Hook.on_tool_create(hook_type="component")
def handle_tool_create_by_component(*args, **kwargs):
    print("math tool component create by component")


@Hook.on_tool_create(hook_type="instance")
def handle_tool_create_by_instance(*args, **kwargs):
    print("math tool component create by instance")


def main():
    hooks = [handle_tool_create_by_instance]
    tool = Calculator(hooks=hooks)
    result = tool.run("6的五次方等于多少")
    print(result)


if __name__ == "__main__":
    main()
