import json
from typing import Optional

from promptulate import BaseMessage, MessageSet
from promptulate.beta.agents.assistant_agent.agent import AssistantAgent
from promptulate.beta.agents.assistant_agent.schema import (
    AgentPlanResponse,
    Plan,
)
from promptulate.llms.base import BaseLLM


class FakeLLM(BaseLLM):
    def _predict(
        self, messages: MessageSet, *args, **kwargs
    ) -> Optional[type(BaseMessage)]:
        return None

    def __call__(self, instruction: str, *args, **kwargs):
        return "FakeLLM output"


def fake_tool_1():
    """Fake tool 1"""
    return "Fake tool 1 output"


def test_init_assistant_agent():
    llm: BaseLLM = FakeLLM()
    agent = AssistantAgent(llm=llm, tools=[fake_tool_1])

    assert len(agent.tool_manager.tools) == 1


def test_schema():
    raw_data = """{\n  \"goals\": [\"Find the hometown of the 2024 Australian Open winner\"],\n  \"tasks\": [\n    {\n      \"task_id\": 1,\n      \"description\": \"Identify the winner of the 2024 Australian Open.\"\n    },\n    {\n      \"task_id\": 2,\n      \"description\": \"Search for the biography or profile of the identified winner.\"\n    },\n    {\n      \"task_id\": 3,\n      \"description\": \"Locate the section of the biography or profile that specifies the player's hometown.\"\n    },\n    {\n      \"task_id\": 4,\n      \"description\": \"Record the hometown of the 2024 Australian Open winner.\"\n    }\n  ]\n}"""  # noqa
    json_data = json.loads(raw_data)
    plan_resp = AgentPlanResponse(**json_data)

    plan = Plan.parse_obj({**plan_resp.dict(), "next_task_id": 1})
    assert plan.next_task_id == 1
