from unittest import TestCase, mock

from promptulate.llms.openai import ChatOpenAI, OpenAI


class TestOpenAI(TestCase):
    @mock.patch("requests.post")
    def test_call(self, mock_post):
        # Mock the API response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"text": "[start] This is a test [end]"}]
        }
        mock_post.return_value = mock_response

        llm = OpenAI()
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test [end]
        ```
        """
        result = llm(prompt)
        self.assertIsNotNone(result)
        self.assertTrue("[start] This is a test [end]" in result)

    @mock.patch("requests.post")
    def test_call_with_stop(self, mock_post):
        # Mock the API response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"text": "[start] This is a test"}]
        }
        mock_post.return_value = mock_response

        llm = OpenAI(temperature=0)
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test [end]
        ```
        """
        result = llm(prompt, stop=["test"])
        self.assertIsNotNone(result)
        self.assertTrue("[start] This is a test" == result)

    def test_generate_prompt_by_retry(self):
        pass


class TestOpenAIChat(TestCase):
    @mock.patch("requests.post")
    def test_call(self, mock_post):
        # Mock the API response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "[start] This is a test [end]"}}]
        }
        mock_post.return_value = mock_response

        llm = ChatOpenAI()
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test [end]
        ```
        """
        result = llm(prompt)
        self.assertIsNotNone(result)
        self.assertTrue("[start] This is a test [end]" in result)

    @mock.patch("requests.post")
    def test_call_with_stop(self, mock_post):
        # Mock the API response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "[start] This is a test"}}]
        }
        mock_post.return_value = mock_response

        llm = ChatOpenAI()
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test
        ```
        """
        result = llm(prompt, stop=["test"])
        self.assertTrue("[end]" not in result)
        self.assertIsNotNone(result)

    def test_generate_prompt_by_retry(self):
        pass
