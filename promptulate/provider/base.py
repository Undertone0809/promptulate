from typing import Optional

from pydantic import BaseModel

from promptulate.llms.base import BaseLLM
from promptulate.memory.base import BaseChatMemory, MessageSet
from promptulate.schema import BaseMessage


class BaseMixin(BaseModel):
    llm: BaseLLM
    conversation_id: Optional[str]
    memory: BaseChatMemory

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def embed_message(
        self, cur_message: BaseMessage, message_history: MessageSet
    ) -> None:
        message_history.messages.append(cur_message)
        self.memory.save_message_set_to_memory(message_history)
