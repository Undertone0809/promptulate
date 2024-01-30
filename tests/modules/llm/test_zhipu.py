import unittest

from promptulate.llms import ZhiPu


class TestZhiPu(unittest.TestCase):
    def test_glm_4_model(self):
        llm = ZhiPu(model="glm-4")
        answer = llm("Please explain the relationship between gravitational waves and general relativity")
        expected_answer = "The relationship between gravitational waves and general relativity is..."
        self.assertEqual(answer, expected_answer)

    def test_glm_3_turbo_model(self):
        llm = ZhiPu(model="glm-3-turbo")
        answer = llm("Please explain the relationship between gravitational waves and general relativity")
        expected_answer = "The relationship between gravitational waves and general relativity is..."
        self.assertEqual(answer, expected_answer)

    def test_model_config(self):
        model_config = {"temperature": 0.1, "top_p": 0.8}
        llm = ZhiPu(model_config=model_config)
        answer = llm("Please explain the relationship between gravitational waves and general relativity")
        expected_answer = "The relationship between gravitational waves and general relativity is..."
        self.assertEqual(answer, expected_answer)

    def test_stop_words(self):
        model_config = {"stop": ["a"]}
        llm = ZhiPu(model_config=model_config)
        prompt = "Please strictly output the following content. [start] This is a test [end]"
        result = llm(prompt)
        expected_result = "[start] This is a"
        self.assertEqual(result, expected_result)

    def test_stream_output(self):
        model_config = {"stream": True}
        llm = ZhiPu(model_config=model_config)
        response = llm("Who are you?")
        expected_response = ["Response chunk 1", "Response chunk 2", ...]
        for i, chunk in enumerate(response):
            self.assertEqual(chunk, expected_response[i])

if __name__ == "__main__":
    unittest.main()
