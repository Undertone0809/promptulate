from typing import List, Optional

from promptulate.pydantic_v1 import BaseModel, Field


class Task(BaseModel):
    task_id: int = Field(..., description="The ID of the task. Start from 1.")
    description: str = Field(..., description="The description of the task.")


class AgentPlanResponse(BaseModel):
    goals: List[str] = Field(..., description="List of goals in the plan.")
    tasks: List[Task] = Field(
        ..., description="List of tasks in the plan, should be in sorted order"
    )


class Plan(AgentPlanResponse):
    next_task_id: Optional[int] = Field(
        ..., description="The ID of the next task, null if no more tasks are needed."
    )

    def get_next_task(self) -> Optional[Task]:
        if self.next_task_id is None:
            return None
        return next((t for t in self.tasks if t.task_id == self.next_task_id), None)


class AgentReviseResponse(Plan):
    thought: str = Field(..., description="The thought of the reflect plan.")
    goals: List[str] = Field(..., description="List of goals in the plan.")
    tasks: List[Task] = Field(
        ..., description="List of tasks in the plan, should be in sorted order"
    )
    next_task_id: Optional[int] = Field(
        ..., description="The ID of the next task, null if no more tasks are needed."
    )


plan_examples = [
    AgentPlanResponse(
        goals=["Goal 1"],
        tasks=[
            Task(task_id=1, description="Task 1"),
            Task(task_id=2, description="Task 2"),
        ],
    ),
]
