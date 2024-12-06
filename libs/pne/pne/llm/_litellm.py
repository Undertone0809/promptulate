import json
from typing import Any, Dict, List, Optional, Tuple, TypedDict, TypeVar

import litellm
from pydantic import BaseModel

from pne.llm.base import LLM
from pne.message import AssistantMessage, MessageSet, StreamMessageIterator, UserMessage
from pne.tools.base import ToolTypes
from pne.utils.logger import logger

T = TypeVar("T", bound=BaseModel)


def parse_content(chunk) -> Tuple[str, dict]:
    """Parse the litellm chunk.
    Args:
        chunk: litellm chunk.

    Returns:
        content: The content of the chunk.
        ret_data: The additional data of the chunk.
    """

    content = chunk.choices[0].delta.content
    ret_data = json.loads(json.dumps(chunk.json()))
    return content, ret_data


class ModelConfig(TypedDict, total=False):
    """ModelConfig."""

    max_tokens: int
    temperature: float
    top_p: float
    n: int
    presence_penalty: float
    frequency_penalty: float
    logit_bias: dict
    user: str
    request_timeout: int
    api_base: str
    api_version: str
    api_key: str
    deployment_id: str
    organization: str
    base_url: str
    default_headers: dict
    timeout: int
    seed: int
    max_retries: int
    logprobs: bool
    top_logprobs: int
    extra_headers: dict


class LiteLLM(LLM):
    def __init__(
        self,
        model: str,
        model_config: Optional[ModelConfig] = None,
        tools: Optional[List[ToolTypes]] = None,
        **kwargs,
    ):
        super().__init__(tools=tools, **kwargs)
        self.model: str = model
        self.model_config: ModelConfig = model_config or {}

    def generate(
        self, messages: MessageSet, tools: Optional[List[ToolTypes]] = None
    ) -> AssistantMessage:
        raw_messages: List[Dict[str, Any]] = messages.to_raw()

        # TODO: support tools

        temp_response = litellm.completion(
            model=self.model,
            messages=raw_messages,
            **self.model_config,
            stream=False,
        )

        response = AssistantMessage(
            content=temp_response.choices[0].message.content,
            additional_kwargs=temp_response.json()
            if isinstance(temp_response.json(), dict)
            else json.loads(temp_response.json()),
        )
        logger.debug(
            f"[pne chat] response: {json.dumps(response.additional_kwargs, indent=2)}"
        )
        return response

    def generate_stream(self, messages: MessageSet) -> StreamMessageIterator:
        pass

    def bind_tools(self, tools: List[ToolTypes], *args, **kwargs):
        pass


def web_search(keyword: str) -> str:
    """web search by keyword.

    Args:
        keyword (str): keyword to search.

    Returns:
        str: search result.
    """
    return "result"


def example1_1():
    model = LiteLLM(model="deepseek/deepseek-chat", model_config={"temperature": 0.5})
    model.bind_tools([web_search])

    # call web_search and get the result based on the web_search function
    response: AssistantMessage = model.run(
        [UserMessage(content="tell me about Shanghai weather tomorrow")]
    )
    print(response.content)


def example1_2():
    model = LiteLLM(
        model="deepseek/deepseek-chat",
        model_config={"temperature": 0.5},
        tools=[web_search],
    )

    # call web_search and get the result based on the web_search function
    response: AssistantMessage = model.run(
        [UserMessage(content="tell me about Shanghai weather tomorrow")]
    )
    print(response.content)


def example1_3():
    model = LiteLLM(
        model="deepseek/deepseek-chat",
        model_config={"temperature": 0.5},
    )

    # call web_search and get the result based on the web_search function
    response: AssistantMessage = model.run(
        [{"role": "user", "content": "tell me about Shanghai weather tomorrow"}],
        tools=[web_search],
    )
    print(response.content)


def example2_1():
    model = LiteLLM(model="deepseek/deepseek-chat", model_config={"temperature": 0.5})
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who are you?"},
    ]

    response: AssistantMessage = model.run(messages)
    print(response.content)


def example2_2():
    model = LiteLLM(model="deepseek/deepseek-chat", model_config={"temperature": 0.5})
    response: AssistantMessage = model.run(
        [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who are you?"},
        ]
    )
    print(response.content)


def example3():
    class LLMResponse(BaseModel):
        cities: List[str]

    model = LiteLLM(model="deepseek/deepseek-chat", model_config={"temperature": 0.5})

    response: LLMResponse = model.run_with_structured(
        messages="Please tell me all provinces in China.",
        response_format=LLMResponse,
    )
    print(response.cities)


def example4():
    class LLMResponse(BaseModel):
        cities: List[str]

    examples = [
        LLMResponse(cities=["Shanghai", "Beijing"]),
        LLMResponse(cities=["Guangzhou", "Shenzhen"]),
    ]

    model = LiteLLM(
        model="deepseek/deepseek-chat",
        model_config={"temperature": 0.5},
        tools=[web_search],
    )

    # get error when using tools, cannot use tools in run_with_structured
    response: LLMResponse = model.run_with_structured(
        messages="Please tell me all provinces in China.",
        response_format=LLMResponse,
    )


def example5():
    from dotenv import load_dotenv
    from pydantic import BaseModel, Field
    import os

    load_dotenv("../../../../.env")

    print("start")

    model = LiteLLM(
        "deepseek/deepseek-chat",
        model_config={
            "temperature": 0.5,
            "api_key": os.environ["DEEPSEEK_API_KEY"],
        },
    )

    class LLMResponse(BaseModel):
        cities: list[str] = Field(..., description="list of cities")

    response: LLMResponse = model.run_with_structured(
        [{"role": "user", "content": "Please tell me 3 provinces in China."}],
        response_format=LLMResponse,
    )
    print(response.cities)


if __name__ == "__main__":
    example5()
