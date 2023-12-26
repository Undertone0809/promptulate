from unittest import TestCase

from promptulate.agents import ToolAgent
from promptulate.hook import Hook
from promptulate.llms import ErnieBot
from promptulate.tools import Calculator, DuckDuckGoTool


class TestToolHook(TestCase):
    def test_instance_hook(self):
        create_flag = False
        start_flag = False
        result_flag = False
        action_flag = False

        @Hook.on_agent_create(hook_type="instance")
        def handle_create(*args, **kwargs):
            nonlocal create_flag
            create_flag = True

        @Hook.on_agent_start(hook_type="instance")
        def handle_start(*args, **kwargs):
            nonlocal start_flag
            start_flag = True

            inputs = args[0]
            self.assertIsNotNone(inputs)
            print(f"<instance> input: {inputs}")

        @Hook.on_agent_action(hook_type="instance")
        def handle_action(*args, **kwargs):
            nonlocal action_flag
            action_flag = True

            thought = kwargs["thought"]
            action = kwargs["action"]
            action_input = kwargs["action_input"]
            self.assertIsNotNone(thought)
            self.assertIsNotNone(action)
            self.assertIsNotNone(action_input)
            print(f"<instance> thought: {thought}")
            print(f"<instance> action: {action}")
            print(f"<instance> action_input: {action_input}")

        @Hook.on_agent_result(hook_type="instance")
        def handle_result(*args, **kwargs):
            nonlocal result_flag
            result_flag = True

            result = kwargs["result"]
            self.assertIsNotNone(result)
            print(f"<instance> result: {result}")

        hooks = [handle_create, handle_start, handle_result]
        tools = [DuckDuckGoTool(), Calculator()]
        agent = ToolAgent(tools=tools, hooks=hooks)
        agent.run("What is promptulate?")

        self.assertTrue(create_flag)
        self.assertTrue(start_flag)
        self.assertTrue(action_flag)
        self.assertTrue(result_flag)

    def test_component_hook(self):
        create_flag = False
        start_flag = False
        result_flag = False
        action_flag = False

        @Hook.on_agent_create(hook_type="component")
        def handle_create(*args, **kwargs):
            nonlocal create_flag
            create_flag = True

        @Hook.on_agent_start(hook_type="component")
        def handle_start(*args, **kwargs):
            nonlocal start_flag
            start_flag = True

            inputs = args[0]
            self.assertIsNotNone(inputs)
            print(f"<component> input: {inputs}")

        @Hook.on_agent_action(hook_type="component")
        def handle_action(*args, **kwargs):
            nonlocal action_flag
            action_flag = True

            thought = kwargs["thought"]
            action = kwargs["action"]
            action_input = kwargs["action_input"]
            self.assertIsNotNone(thought)
            self.assertIsNotNone(action)
            self.assertIsNotNone(action_input)
            print(f"<component> thought: {thought}")
            print(f"<component> action: {action}")
            print(f"<component> action_input: {action_input}")

        @Hook.on_agent_result(hook_type="component")
        def handle_result(*args, **kwargs):
            nonlocal result_flag
            result_flag = True

            result = kwargs["result"]
            self.assertIsNotNone(result)
            print(f"<component> result: {result}")

        tools = [DuckDuckGoTool(), Calculator()]
        agent = ToolAgent(tools=tools)
        agent.run("What is promptulate?")

        self.assertTrue(create_flag)
        self.assertTrue(start_flag)
        self.assertTrue(action_flag)
        self.assertTrue(result_flag)
