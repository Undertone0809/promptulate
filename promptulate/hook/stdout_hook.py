from promptulate.hook import Hook, HookTable
from promptulate.utils.color_print import print_text


class StdOutHook:
    @staticmethod
    def handle_agent_start(*args, **kwargs):
        print_text("Agent Start...", "red")
        print_text(f"[User] {args[0]}", "blue")

    @staticmethod
    def handle_agent_action(*args, **kwargs):
        print_text(f"[Thought] {kwargs['thought']}", "yellow")
        print_text(
            f"[Action] {kwargs['action']} args: {kwargs['action_input']}", "yellow"
        )

    @staticmethod
    def handle_agent_observation(*args, **kwargs):
        print_text(f"[Observation] {kwargs['observation']}", "yellow")

    @staticmethod
    def handle_agent_result(*args, **kwargs):
        print_text(f"[Agent Result] {kwargs['result']}", "green")
        print_text("Agent End.", "pink")

    @staticmethod
    def registry_stdout_hooks():
        """Registry and enable stdout hooks. StdoutHook can print colorful
        information."""
        Hook.registry_hook(
            HookTable.ON_AGENT_START, StdOutHook.handle_agent_start, "component"
        )
        Hook.registry_hook(
            HookTable.ON_AGENT_ACTION, StdOutHook.handle_agent_action, "component"
        )
        Hook.registry_hook(
            HookTable.ON_AGENT_OBSERVATION,
            StdOutHook.handle_agent_observation,
            "component",
        )
        Hook.registry_hook(
            HookTable.ON_AGENT_RESULT, StdOutHook.handle_agent_result, "component"
        )

    @staticmethod
    def unregister_stdout_hooks():
        Hook.unregister_hook(StdOutHook.handle_agent_start)
        Hook.unregister_hook(StdOutHook.handle_agent_action)
        Hook.unregister_hook(StdOutHook.handle_agent_observation)
        Hook.unregister_hook(StdOutHook.handle_agent_result)
