from unittest import TestCase

from promptulate.hook import Hook
from promptulate.llms import ChatOpenAI
from promptulate.utils.logger import enable_log

enable_log()


class TestLLMHook(TestCase):
    def test_instance_hook(self):
        create_flag = False
        start_flag = False
        result_flag = False

        @Hook.on_llm_create(hook_type="instance")
        def handle_create(*args, **kwargs):
            nonlocal create_flag
            create_flag = True

        @Hook.on_llm_start(hook_type="instance")
        def handle_start(*args, **kwargs):
            nonlocal start_flag
            start_flag = True

            prompt = args[0]
            self.assertIsNotNone(prompt)
            print(prompt)

        @Hook.on_llm_result(hook_type="instance")
        def handle_result(*args, **kwargs):
            nonlocal result_flag
            result_flag = True

            result = kwargs["result"]
            self.assertIsNotNone(result)
            print(result)

        hooks = [handle_create, handle_start, handle_result]
        llm = ChatOpenAI(hooks=hooks)
        llm("What is LLM?")

        self.assertTrue(create_flag)
        self.assertTrue(start_flag)
        self.assertTrue(result_flag)

    def test_component_hook(self):
        create_flag = False
        start_flag = False
        result_flag = False

        @Hook.on_llm_create(hook_type="component")
        def handle_create(*args, **kwargs):
            nonlocal create_flag
            create_flag = True

        @Hook.on_llm_start(hook_type="component")
        def handle_start(*args, **kwargs):
            nonlocal start_flag
            start_flag = True

            prompt = args[0]
            self.assertIsNotNone(prompt)
            print(prompt)

        @Hook.on_llm_result(hook_type="component")
        def handle_result(*args, **kwargs):
            nonlocal result_flag
            result_flag = True

            result = kwargs["result"]
            self.assertIsNotNone(result)
            print(result)

        llm = ChatOpenAI()
        llm("What is LLM?")

        self.assertTrue(create_flag)
        self.assertTrue(start_flag)
        self.assertTrue(result_flag)
