from enum import Enum
from typing import Callable, Dict, List, Optional, TypedDict

from typing_extensions import NotRequired

from promptulate import uacp
from promptulate.agents.assistant_agent import operations
from promptulate.agents.assistant_agent.schema import Plan
from promptulate.agents.base import BaseAgent
from promptulate.agents.tool_agent import ToolAgent
from promptulate.agents.tool_agent.agent import ActionResponse
from promptulate.hook import Hook, HookTable
from promptulate.llms.base import BaseLLM
from promptulate.tools.base import ToolTypes
from promptulate.tools.manager import ToolManager
from promptulate.utils.logger import logger


class StepTypes(str, Enum):
    PLAN = "plan"
    EXECUTE = "execute"
    REVISE = "revise"


class AdditionalProperties(TypedDict):
    current_plan: dict
    past_steps: NotRequired[str]


class AssistantAgent(BaseAgent):
    """
    An agent who can plan, execute, and revise tasks.
    """

    def __init__(
        self,
        *,
        llm: BaseLLM,
        tools: Optional[List[ToolTypes]] = None,
        max_iterations: Optional[int] = 20,
        **kwargs,
    ):
        super().__init__(agent_type="Assistant Agent", **kwargs)

        self.llm = llm
        self.tool_manager = ToolManager(tools=tools if tools else [])
        self.tool_agent = ToolAgent(
            llm=llm, tool_manager=self.tool_manager, _from="agent"
        )
        self.uacp_agent = uacp.Agent(
            self.task_handler, self.step_handler, self.result_handler
        )
        self.current_task_id: Optional[str] = None
        self.max_iterations: int = max_iterations

        logger.info("Assistant Agent initialized.")

    def _run(
        self, instruction: str, additional_input: dict = None, *args, **kwargs
    ) -> str:
        additional_input = additional_input or {}

        result: str = self.uacp_agent.run(
            input=instruction, additional_input=additional_input
        )
        logger.info(f"Assistant Agent response: {result}")
        return result

    def get_llm(self) -> BaseLLM:
        return self.llm

    @property
    def current_task(self) -> Optional[uacp.Task]:
        """Get the current task, return None if no task is running."""
        if self.current_task_id is None:
            return None

        return self.uacp_agent.db.get_task(self.current_task_id)

    @property
    def current_plan(self) -> Optional[Plan]:
        """Get the current plan. Every step has a current plan stored in
        additional_properties."""
        if self.current_task is None:
            return None

        _: dict = self.current_task.steps[-1].additional_properties.get("current_plan")
        return Plan.parse_obj(_)

    @property
    def execution_steps(self) -> List[uacp.Step]:
        """Get the execution steps from the current task."""
        if self.current_task is None:
            return []

        return [s for s in self.current_task.steps if s.name == StepTypes.EXECUTE]

    def plan(self, step: uacp.Step) -> uacp.Step:
        """Plan the task and create the next step: execute.

        Args:
            step(uacp.Step): The current step.

        Returns:
            uacp.Step: The updated plan step.
        """
        logger.info("[Assistant Agent] Planning now.")

        current_plan: Plan = operations.plan(self.llm, step.input)
        Hook.call_hook(HookTable.ON_AGENT_PLAN, self, plan=current_plan.json())

        # create next step: execute
        task = self.uacp_agent.db.get_task(step.task_id)

        self.uacp_agent.db.create_step(
            task_id=task.task_id,
            name=StepTypes.EXECUTE,
            input=current_plan.tasks[0].description,
            additional_properties=AdditionalProperties(
                current_plan=current_plan.dict()
            ),
        )
        step.output = current_plan.json()

        return step

    def execute(self, step: uacp.Step) -> uacp.Step:
        """Execute the plan and create the next step: revise.

        Args:
            step(uacp.Step): The current step.

        Returns:
            uacp.Step: The updated execute step.
        """
        logger.info("[Assistant Agent] Executing step now.")

        resp: ActionResponse = operations.execute(self.tool_agent, step.input)

        if self.current_plan.get_next_task() is None:
            step.is_last = True
            step.output = resp["action_parameters"]["content"]
            return step

        # create next step: revise
        self.uacp_agent.db.create_step(
            task_id=step.task_id,
            name=StepTypes.REVISE,
            input=resp["action_parameters"]["content"],
            additional_properties=AdditionalProperties(
                current_plan=self.current_plan.dict(),
                past_steps=str(resp),
            ),
        )

        step.output = str(resp)
        return step

    def revise(self, step: uacp.Step) -> uacp.Step:
        """Review the plan and update the plan accordingly. This behavior will decide if
         the plan is complete or not, and if not, will update the plan accordingly.

        Args:
            step(uacp.Step): The current step.

        Returns:
            uacp.Step: The updated revise step.
        """
        logger.info("[Assistant Agent] Reviewing now.")

        revised_plan: Plan = operations.revise(
            llm=self.llm,
            user_target=self.current_task.input,
            original_plan=self.current_plan.json(),
            past_steps=step.additional_properties["past_steps"],
        )

        Hook.call_hook(
            HookTable.ON_AGENT_REVISE_PLAN, self, revised_plan=revised_plan.json()
        )

        if revised_plan.get_next_task() is None:
            step.is_last = True
            step.output = step.input
            return step
        else:
            # create next step: execute
            task = self.uacp_agent.db.get_task(step.task_id)
            self.uacp_agent.db.create_step(
                task_id=task.task_id,
                name=StepTypes.EXECUTE,
                input=revised_plan.get_next_task().description,
                additional_properties=AdditionalProperties(
                    current_plan=revised_plan.dict()
                ),
            )

            step.output = revised_plan.json()

        return step

    def task_handler(self, task: uacp.Task) -> None:
        """Invoke the task and start planning.

        Args:
            task: Task object
        """
        if not task.input:
            raise Exception("No task prompt")

        logger.info(
            f"[Assistant Agent] Task received. Creating Plan step, task input: {task.input}"  # noqa
        )
        self.current_task_id = task.task_id
        self.uacp_agent.db.create_step(
            task_id=task.task_id, name=StepTypes.PLAN, input=task.input
        )

    def step_handler(self, step: uacp.Step) -> uacp.Step:
        logger.info(
            f"[Assistant Agent] Step received. Executing step, step name: {step.name}"
        )
        step_map: Dict[str, Callable] = {
            StepTypes.PLAN: self.plan,
            StepTypes.EXECUTE: self.execute,
            StepTypes.REVISE: self.revise,
        }

        if len(self.current_task.steps) > self.max_iterations:
            final_output: str = self.current_task.steps[-1].output
            step.output = f"Task has too many steps. Aborting. Recently step output: {final_output}"  # noqa
            return step

        if step.name not in step_map:
            raise ValueError(f"Step name {step.name} not found in step mapping.")

        return step_map[step.name](step)

    def result_handler(self, uacp_task: uacp.Task) -> str:
        return uacp_task.steps[-1].output
