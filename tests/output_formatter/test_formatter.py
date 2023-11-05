from typing import Optional

from pydantic import BaseModel, Field

from promptulate.agents import BaseAgent
from promptulate.llms import BaseLLM
from promptulate.output_formatter import OutputFormatter
from promptulate.schema import BaseMessage, MessageSet


class LLMForTest(BaseLLM):
    llm_type: str = "custom_llm"

    def _predict(self, prompts: MessageSet, *args, **kwargs) -> Optional[BaseMessage]:
        pass

    def __call__(self, *args, **kwargs):
        return """## Output
        ```json
        {
          "city": "Shanghai",
          "temperature": 25
        }
        ```"""


class AgentForTest(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm = LLMForTest()

    def get_llm(self) -> BaseLLM:
        return self.llm

    def _run(self, prompt: str, *args, **kwargs) -> str:
        return ""


class Response(BaseModel):
    city: str = Field(description="City name")
    temperature: float = Field(description="Temperature in Celsius")


def test_formatter_with_llm():
    llm = LLMForTest()
    formatter = OutputFormatter(Response)

    prompt = f"What is the temperature in Shanghai tomorrow? \n{formatter.get_formatted_instructions()}"
    llm_output = llm(prompt)
    response: Response = formatter.formatting_result(llm_output)
    assert isinstance(response, Response)
    assert isinstance(response.city, str)
    assert isinstance(response.temperature, float)


def test_formatter_with_agent():
    agent = AgentForTest()
    prompt = f"What is the temperature in Shanghai tomorrow?"
    response: Response = agent.run(prompt=prompt, output_schema=Response)
    assert isinstance(response, Response)
    assert isinstance(response.city, str)
    assert isinstance(response.temperature, float)
