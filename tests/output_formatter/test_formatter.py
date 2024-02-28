from typing import Optional

import pytest

from promptulate.agents import BaseAgent
from promptulate.llms import BaseLLM
from promptulate.output_formatter import OutputFormatter, formatting_result
from promptulate.pydantic_v1 import BaseModel, Field
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


class LLMResponse(BaseModel):
    city: str = Field(description="City name")
    temperature: float = Field(description="Temperature in Celsius")


def test_formatter_with_llm():
    llm = LLMForTest()
    formatter = OutputFormatter(LLMResponse)

    prompt = (
        f"What is the temperature in Shanghai tomorrow? \n"
        f"{formatter.get_formatted_instructions()}"
    )
    llm_output = llm(prompt)
    response: LLMResponse = formatter.formatting_result(llm_output)
    assert isinstance(response, LLMResponse)
    assert isinstance(response.city, str)
    assert isinstance(response.temperature, float)


def test_formatter_with_agent():
    agent = AgentForTest()
    prompt = "What is the temperature in Shanghai tomorrow?"
    response: LLMResponse = agent.run(prompt=prompt, output_schema=LLMResponse)
    assert isinstance(response, LLMResponse)
    assert isinstance(response.city, str)
    assert isinstance(response.temperature, float)


def test_init_outputformatter_with_error_pydantic_type():
    """Test the error when the pydantic_obj of OutputFormatter is not a Pydantic
    object."""

    with pytest.raises(ValueError) as excinfo:
        OutputFormatter("test")

    assert "pydantic_obj must be a Pydantic object" in str(excinfo.value)


def test_formatting_result_with_error_llm_output():
    """Test the error when the llm_output of formatting_result is not a valid
    json."""

    from promptulate.error import OutputParserError

    with pytest.raises(OutputParserError) as excinfo:
        formatting_result(LLMResponse, "test")

    assert f"Failed to parse {LLMResponse.__name__} from completion test." in str(
        excinfo.value
    )
