from promptulate.agents.tool_agent.agent import ActionResponse, ToolAgent
from promptulate.beta.agents.assistant_agent.prompt import (
    PLAN_SYSTEM_PROMPT_TMP,
    REVIEW_SYSTEM_PROMPT_TMP,
)
from promptulate.beta.agents.assistant_agent.schema import (
    AgentPlanResponse,
    AgentReviseResponse,
    Plan,
    plan_examples,
)
from promptulate.llms.base import BaseLLM
from promptulate.output_formatter import OutputFormatter


def plan(llm: BaseLLM, user_target: str) -> Plan:
    """Generate a plan for the user target."""
    system_prompt = PLAN_SYSTEM_PROMPT_TMP.format(user_target=user_target)
    formatter = OutputFormatter(AgentPlanResponse, plan_examples)
    system_prompt += formatter.get_formatted_instructions()

    resp: str = llm(instruction=system_prompt)
    plan_resp: AgentPlanResponse = formatter.formatting_result(resp)

    return Plan.parse_obj({**plan_resp.dict(), "next_task_id": 1})


def execute(tool_agent: ToolAgent, user_target: str) -> ActionResponse:
    """Execute the plan for the user target."""
    return tool_agent.run(user_target, return_raw_data=True)


def revise(llm: BaseLLM, user_target: str, original_plan: str, past_steps: str) -> Plan:
    system_prompt = REVIEW_SYSTEM_PROMPT_TMP.format(
        user_target=user_target,
        original_plan=original_plan,
        past_steps=past_steps,
    )
    formatter = OutputFormatter(AgentReviseResponse, plan_examples)
    system_prompt += formatter.get_formatted_instructions()

    resp: str = llm(instruction=system_prompt)
    plan_resp: AgentReviseResponse = formatter.formatting_result(resp)

    return Plan.parse_obj({**plan_resp.dict()})
