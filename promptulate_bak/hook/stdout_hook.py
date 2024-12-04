from promptulate.hook import Hook, HookTable
from promptulate.utils.color_print import print_text


class StdOutHook:
    @staticmethod
    def handle_agent_start(*args, **kwargs):
        if kwargs.get("agent_type", None):
            print_text(f"[Agent] {kwargs['agent_type']} start...", "red")
        else:
            print_text("[Agent] Agent Start...", "red")

        if kwargs.get("_from", None) is None:
            print_text(f"[User instruction] {args[0]}", "blue")
        elif kwargs["_from"] == "agent":
            print_text(f"[Agent execution] {args[0]}", "blue")

    @staticmethod
    def handle_agent_plan(*args, **kwargs):
        print_text(f"[Plan] {kwargs['plan']}", "green")

    @staticmethod
    def handle_agent_revise_plan(*args, **kwargs):
        print_text(f"[Revised Plan] {kwargs['revised_plan']}", "green")

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
        if kwargs.get("_from", None) is None:
            print_text(f"[Agent Result] {kwargs['result']}", "green")
            print_text("[Agent] Agent End.", "pink")
        elif kwargs["_from"] == "agent":
            print_text(f"[Execute Result] {kwargs['result']}", "green")
            print_text("[Execute] Execute End.", "pink")

    @staticmethod
    def registry_stdout_hooks():
        """Registry and enable stdout hooks. StdoutHook can print colorful
        information."""
        Hook.registry_hook(
            HookTable.ON_AGENT_START, StdOutHook.handle_agent_start, "component"
        )
        Hook.registry_hook(
            HookTable.ON_AGENT_PLAN, StdOutHook.handle_agent_plan, "component"
        )
        Hook.registry_hook(
            HookTable.ON_AGENT_REVISE_PLAN,
            StdOutHook.handle_agent_revise_plan,
            "component",
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
