import os
from typing import Any, Callable, Optional

from promptulate.uacp.db import InMemoryTaskDB, TaskDB
from promptulate.uacp.schema import Status, Step, Task
from promptulate.utils.logger import logger

StepHandler = Callable[[Step], Step]
TaskHandler = Callable[[Task], None]
ResultHandler = Callable[[Task], Any]

_task_handler: Optional[TaskHandler]
_step_handler: Optional[StepHandler]


class Agent:
    def __init__(
        self,
        task_handler: TaskHandler,
        step_handler: StepHandler,
        result_handler: ResultHandler,
        *,
        db: TaskDB = None,
        workspace: str = None,
    ):
        self.task_handler: TaskHandler = task_handler
        self.step_handler: StepHandler = step_handler
        self.result_handler: ResultHandler = result_handler
        self.db: TaskDB = db or InMemoryTaskDB()
        self.workspace: str = workspace or os.getenv("AGENT_WORKSPACE", "workspace")

    def run(
        self,
        input: Optional[str] = None,
        additional_input: Optional[dict] = None,
    ) -> Any:
        task = self.db.create_task(input=input, additional_input=additional_input)
        self.task_handler(task)

        # step handler
        task = self.db.get_task(task.task_id)

        if not task.steps:
            raise Exception("No steps to execute")

        while True:
            task = self.db.get_task(task.task_id)
            step: Optional[Step] = next(
                filter(lambda x: x.status == Status.created, task.steps), None
            )

            if step is None:
                break

            step.status = Status.running
            step = self.step_handler(step)
            step.status = Status.completed

            self.db.update_step(task.task_id, step)
            logger.info(f"[uacp] Step {step.name}: {step.json()}")

        # result handler
        task = self.db.get_task(task.task_id)
        task_result: Any = self.result_handler(task)
        self.db.update_task(task)

        return task_result

    def startup_server(self):
        pass
