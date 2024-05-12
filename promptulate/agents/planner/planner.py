from promptulate.agents.assistant_agent.schema import (
    AgentPlanResponse,
    Plan,
    plan_examples,
)
from promptulate.agents.planner.prompt import PLAN_SYS_PROMPT
from promptulate.chat import AIChat
from promptulate.llms.base import BaseLLM
from promptulate.output_formatter import OutputFormatter


class Planner:
    def __init__(self, llm: BaseLLM, system_prompt: str):
        self.ai = AIChat(custom_llm=llm)
        self.system_prompt: str = system_prompt

    def run(self, instruction: str) -> Plan:
        """Generate a plan for the user target."""
        system_prompt = PLAN_SYS_PROMPT + instruction
        formatter = OutputFormatter(AgentPlanResponse, plan_examples)
        system_prompt += formatter.get_formatted_instructions()

        resp: str = self.ai.run(system_prompt)
        plan_resp: AgentPlanResponse = formatter.formatting_result(resp)

        return Plan.parse_obj({**plan_resp.dict(), "next_task_id": 1})
