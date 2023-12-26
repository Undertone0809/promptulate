from unittest import TestCase, mock

from promptulate.hook import Hook
from promptulate.llms import ChatOpenAI


class TestLLMHook(TestCase):

    @mock.patch("requests.post")
    def test_instance_hook(self, mock_post):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "LLM is large language model."}}]
        }
        mock_post.return_value = mock_response

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

    @mock.patch("requests.post")
    def test_component_hook(self, mock_post):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "LLM is large language model."}}]
        }
        mock_post.return_value = mock_response

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
