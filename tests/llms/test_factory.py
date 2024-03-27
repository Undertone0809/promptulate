from unittest import TestCase, mock

import promptulate as pne


class TestLLMFactory(TestCase):
    @mock.patch("requests.post")
    def test_call(self, mock_post):
        # Mock the API response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "[start] This is a test [end]"}}]
        }
        mock_post.return_value = mock_response

        llm = pne.LLMFactory.build("zhipu")
        llm.set_private_api_key("my key.hello")
        prompt = """
        Please strictly output the following content.
        ```
        [start] This is a test [end]
        ```
        """
        result = llm(prompt)
        self.assertIsNotNone(result)
        self.assertTrue("[start] This is a test [end]" in result)
