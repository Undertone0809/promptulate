import uuid
from abc import ABC
from typing import Any, Dict, List, Optional, Union

from promptulate.uacp.schema import Artifact, Status, Step, Task
from promptulate.utils.logger import logger


class TaskDB(ABC):
    def create_task(
        self,
        input: Optional[str],
        additional_input: Any = None,
        artifacts: Optional[List[Artifact]] = None,
        steps: Optional[List[Step]] = None,
    ) -> Task:
        raise NotImplementedError

    def create_step(
        self,
        task_id: str,
        name: Optional[str] = None,
        input: Optional[str] = None,
        is_last: bool = False,
        additional_properties: Optional[Dict[str, Any]] = None,
        artifacts: Optional[List[Artifact]] = None,
    ) -> Step:
        raise NotImplementedError

    def create_artifact(
        self,
        task_id: str,
        file_name: str,
        agent_created: bool = True,
        relative_path: Optional[str] = None,
        step_id: Optional[str] = None,
    ) -> Artifact:
        raise NotImplementedError

    def get_task(self, task_id: str) -> Task:
        raise NotImplementedError

    def get_step(self, task_id: str, step_id: str) -> Step:
        raise NotImplementedError

    def get_artifact(self, task_id: str, artifact_id: str) -> Artifact:
        raise NotImplementedError

    def update_task(self, task: Task) -> Task:
        raise NotImplementedError

    def update_step(self, task_id: str, step: Step) -> Step:
        raise NotImplementedError

    def list_tasks(self) -> List[Task]:
        raise NotImplementedError

    def list_steps(self, task_id: str, status: Optional[Status] = None) -> List[Step]:
        raise NotImplementedError


class InMemoryTaskDB(TaskDB):
    _tasks: Dict[str, Task] = {}

    def create_task(
        self,
        input: Optional[str],
        additional_input: Any = None,
        artifacts: Optional[List[Artifact]] = None,
        steps: Optional[List[Step]] = None,
    ) -> Task:
        steps = steps or []
        artifacts = artifacts or []
        task_id = str(uuid.uuid4())

        task = Task(
            task_id=task_id,
            input=input,
            steps=steps,
            artifacts=artifacts,
            additional_input=additional_input,
        )
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Task:
        task = self._tasks.get(task_id, None)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return task

    def update_task(self, task: Task) -> Task:
        if self._tasks.get(task.task_id, None) is None:
            raise ValueError(f"Task {task.task_id} not found")
        self._tasks[task.task_id] = task
        return task

    def create_step(
        self,
        task_id: str,
        name: Optional[str] = None,
        input: Optional[str] = None,
        is_last=False,
        additional_properties: Optional[Dict[str, Any]] = None,
        artifacts: Optional[List[Artifact]] = None,
    ) -> Step:
        step_id: str = str(uuid.uuid4())
        artifacts: List[Artifact] = artifacts or []

        step = Step(
            task_id=task_id,
            step_id=step_id,
            name=name,
            input=input,
            status=Status.created,
            is_last=is_last,
            additional_properties=additional_properties,
            artifacts=artifacts,
        )
        logger.info(f"Create step: {step.json()}")
        task = self.get_task(task_id)
        task.steps.append(step)
        return step

    def get_step(self, task_id: str, step_id: str) -> Step:
        task = self.get_task(task_id)
        step = next(filter(lambda s: s.task_id == task_id, task.steps), None)
        if not step:
            raise ValueError(f"Step {step_id} not found in task {task_id}")
        return step

    def update_step(self, task_id: str, step: Step) -> Step:
        task = self.get_task(task_id)

        for i, s in enumerate(task.steps):
            if s.step_id == step.step_id:
                task.steps[i] = step
                return step

        raise ValueError(f"Step {step.step_id} not found in task {task_id}")

    def create_artifact(
        self,
        task_id: str,
        file_name: str,
        agent_created: bool = True,
        relative_path: Optional[str] = None,
        step_id: Optional[str] = None,
    ) -> Artifact:
        artifact_id = str(uuid.uuid4())
        artifact = Artifact(
            artifact_id=artifact_id,
            agent_created=agent_created,
            file_name=file_name,
            relative_path=relative_path,
        )
        task = self.get_task(task_id)
        task.artifacts.append(artifact)

        if step_id:
            step = self.get_step(task_id, step_id)
            step.artifacts.append(artifact)

        return artifact

    def get_artifact(self, task_id: str, artifact_id: str) -> Artifact:
        task = self.get_task(task_id)
        artifact = next(
            filter(lambda a: a.artifact_id == artifact_id, task.artifacts), None
        )
        if not artifact:
            raise ValueError(f"Artifact {artifact_id} not found in task {task_id}")
        return artifact

    def list_tasks(self) -> List[Task]:
        return [task for task in self._tasks.values()]

    def list_steps(self, task_id: str, status: Optional[Status] = None) -> List[Step]:
        task = self.get_task(task_id)
        steps = task.steps
        if status:
            steps = list(filter(lambda s: s.status == status, steps))
        return steps
