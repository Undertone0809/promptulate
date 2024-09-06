import pne
from mem0 import MemoryClient


class PersonalHealingAssistant:
    def __init__(self):
        self.memory = None
        self.messages = [
            {"role": "system", "content": "You are a personal healing AI Assistant."}
        ]

    def set_mem0_api_key(self, mem0_api_key: str):
        self.memory = MemoryClient(api_key=mem0_api_key)

    def ask_question(self, question: str, user_id: str, config) -> str:
        # Fetch previous related memories
        previous_memories = self.search_memories(question, user_id=user_id)
        prompt = question
        if previous_memories:
            prompt = f"User input: {question}\n Previous memories: {previous_memories}"
        self.messages.append({"role": "user", "content": prompt})

        response = pne.chat(
            model=config.model_name,
            stream=True,
            messages=self.messages,
            model_config={"api_base": config.api_base, "api_key": config.api_key},
        )
        self.messages.append({"role": "assistant", "content": response})

        # Store the question in memory
        self.memory.add(question, user_id=user_id)
        return response

    def get_memories(self, user_id):
        memories = self.memory.get_all(user_id=user_id)
        return memories

    def search_memories(self, query, user_id):
        memories = self.memory.search(query, user_id=user_id)
        return memories
