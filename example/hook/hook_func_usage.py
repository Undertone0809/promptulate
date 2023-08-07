from promptulate.hook import Hook, HookTable
from promptulate.llms import ChatOpenAI


def handle_start_by_instance(*args, **kwargs):
    print(f"llm instance start hook: {args[0]}")


def handle_result_by_instance(*args, **kwargs):
    print(f"llm instance result hook: {kwargs['result']}")


def handle_result_by_component(*args, **kwargs):
    print(f"llm component result hook: {kwargs['result']}")


Hook.registry_hook(HookTable.ON_LLM_START, handle_start_by_instance, "instance")
Hook.registry_hook(HookTable.ON_LLM_RESULT, handle_result_by_instance, "instance")
Hook.registry_hook(HookTable.ON_LLM_RESULT, handle_result_by_component, "component")
hooks = [handle_start_by_instance, handle_result_by_instance]
llm = ChatOpenAI(hooks=hooks)
llm("hello")
