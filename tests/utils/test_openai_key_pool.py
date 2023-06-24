from unittest import TestCase

from promptulate.utils.openai_key_pool import (
    OpenAIKeyPool,
    export_openai_key_pool,
    add_key_to_key_pool,
)


class TestOpenAIKeyPool(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key_pool: OpenAIKeyPool = OpenAIKeyPool()

    def test_set_key_pool(self):
        keys = [
            {"model": "gpt-3.5-turbo", "key": "key1"},
            {"model": "gpt-3.5-turbo", "key": "key2"},
            {"model": "gpt-3.5-turbo", "key": "key3"},
            {"model": "gpt-4", "key": "key4"},
        ]
        self.key_pool.set(keys)
        num = self.key_pool.get_num("gpt-3.5-turbo")
        self.assertEqual(num, 3)
        self.assertEqual(self.key_pool.get("gpt-3.5-turbo"), "key1")
        self.assertEqual(self.key_pool.get("gpt-3.5-turbo"), "key2")
        self.assertEqual(self.key_pool.get("gpt-3.5-turbo"), "key3")
        self.assertEqual(self.key_pool.get("gpt-3.5-turbo"), "key1")
        self.assertEqual(self.key_pool.get("gpt-4"), "key4")

    def test_export_openai_key_pool(self):
        keys = [
            {"model": "gpt-3.5-turbo", "key": "key1"},
            {"model": "gpt-3.5-turbo", "key": "key2"},
            {"model": "gpt-3.5-turbo", "key": "key3"},
            {"model": "gpt-4", "key": "key4"},
        ]
        export_openai_key_pool(keys)
        num = self.key_pool.get_num("gpt-3.5-turbo")
        self.assertEqual(num, 3)
        self.assertEqual(self.key_pool.get("gpt-3.5-turbo"), "key1")
        self.assertEqual(self.key_pool.get("gpt-3.5-turbo"), "key2")
        self.assertEqual(self.key_pool.get("gpt-3.5-turbo"), "key3")
        self.assertEqual(self.key_pool.get("gpt-3.5-turbo"), "key1")
        self.assertEqual(self.key_pool.get("gpt-4"), "key4")

    def test_append_key_pool(self):
        keys = [
            {"model": "gpt-3.5-turbo", "key": "key4"},
            {"model": "gpt-3.5-turbo", "key": "key5"},
            {"model": "gpt-3.5-turbo", "key": "key6"},
            {"model": "gpt-4", "key": "key7"},
        ]
        add_key_to_key_pool(keys)
        num = self.key_pool.get_num("gpt-3.5-turbo")
        self.assertEqual(num, 6)
