# from unittest import TestCase

# from promptulate.frameworks.conversation import Conversation
# from promptulate.memory import FileChatMemory
# from promptulate.utils.logger import enable_log, get_logger

# enable_log()
# logger = get_logger()


# class TestConversation(TestCase):
#     def test_predict(self):
#         conversation = Conversation()
#         result = conversation.run("什么是大语言模型")
#         self.assertIsNotNone(result)
#         self.assertTrue("大语言模型" in result)

#     def test_predict_with_stop(self):
#         conversation = Conversation()
#         prompt = """
#         Please strictly output the following content.
#         ```
#         [start] This is a test [end]
#         ```
#         """
#         result = conversation.run(prompt, stop=["test"])
#         self.assertTrue("test [end]" not in result)
#         self.assertIsNotNone(result)

#     def test_memory_with_buffer(self):
#         conversation = Conversation()
#         prompt = """give me 5 company names"""
#         conversation.run(prompt)
#         conversation_id = conversation.conversation_id
#         new_conversation = Conversation(conversation_id=conversation_id)
#         new_conversation.predict("give me 5 more")

#     def test_memory_with_file(self):
#         conversation = Conversation(memory=FileChatMemory())
#         prompt = """give me 5 company names"""
#         conversation.run(prompt)
#         conversation_id = conversation.conversation_id
#         new_conversation = Conversation(
#             conversation_id=conversation_id, memory=FileChatMemory()
#         )
#         new_conversation.predict("give me 5 more")
