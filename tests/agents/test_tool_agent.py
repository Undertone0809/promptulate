from promptulate.agents.tool_agent.agent import ToolAgent
from promptulate.llms.base import BaseLLM
from promptulate.tools.base import BaseToolKit


class FakeLLM(BaseLLM):
    def _predict(self, prompts, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return """## Output
        ```json
        {
          "city": "Shanghai",
          "temperature": 25
        }
        ```"""


def fake_tool_1():
    """Fake tool 1"""
    return "Fake tool 1"


def fake_tool_2():
    """Fake tool 2"""
    return "Fake tool 2"


def test_init():
    llm = FakeLLM()
    agent = ToolAgent(llm=llm)
    assert len(agent.tool_manager.tools) == 0

    agent = ToolAgent(llm=llm, tools=[fake_tool_1, fake_tool_2])
    assert len(agent.tool_manager.tools) == 2
    assert agent.tool_manager.tools[0].name == "fake_tool_1"
    assert agent.tool_manager.tools[1].name == "fake_tool_2"


class MockToolKit(BaseToolKit):
    def get_tools(self) -> list:
        return [fake_tool_1, fake_tool_2]


def test_init_by_toolkits():
    llm = FakeLLM()
    agent = ToolAgent(llm=llm, tools=[MockToolKit()])
    assert len(agent.tool_manager.tools) == 2


def test_init_by_tool_and_kit():
    llm = FakeLLM()
    agent = ToolAgent(llm=llm, tools=[MockToolKit(), fake_tool_1, fake_tool_2])
    assert len(agent.tool_manager.tools) == 4


def test_stream_mode():
    llm = FakeLLM()
    agent = ToolAgent(llm=llm, tools=[fake_tool_1, fake_tool_2])
    prompt = "What is the temperature in Shanghai?"
    responses = list(agent.run(prompt, stream=True))
    assert len(responses) > 0
    assert all(isinstance(response, str) for response in responses)
