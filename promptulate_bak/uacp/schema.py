from enum import Enum, auto
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Status(Enum):
    created = auto()
    running = auto()
    completed = auto()


class StepOutput(BaseModel):
    pass


class Artifact(BaseModel):
    artifact_id: str = Field(
        ...,
        description="ID of the artifact.",
        examples=["b225e278-8b4c-4f99-a696-8facf19f0e56"],
    )
    agent_created: bool = Field(
        ...,
        description="Whether the artifact has been created by the agent.",
        examples=[False],
    )
    file_name: str = Field(
        ..., description="Filename of the artifact.", examples=["main.py"]
    )
    relative_path: Optional[str] = Field(
        None,
        description="Relative path of the artifact in the agent's workspace.",
        examples=["python/code/"],
    )


class StepRequestBody(BaseModel):
    input: Optional[str] = Field(
        None,
        description="Input prompt for the step.",
        examples=["Write the words you receive to the file 'output.txt'."],
    )
    additional_input: Optional[Dict[str, Any]] = None


class Step(StepRequestBody):
    task_id: str = Field(
        ...,
        description="The ID of the task this step belongs to.",
        examples=["50da533e-3904-4401-8a07-c49adf88b5eb"],
    )
    step_id: str = Field(
        ...,
        description="The ID of the task step.",
        examples=["6bb1801a-fd80-45e8-899a-4dd723cc602e"],
    )
    name: Optional[str] = Field(
        None, description="The name of the task step.", examples=["Write to file"]
    )
    status: Status = Field(
        ..., description="The status of the task step.", examples=["created"]
    )
    output: Optional[str] = Field(
        None,
        description="Output of the task step.",
        examples=[
            "I am going to use the write_to_file command and write Washington to a file called output.txt <write_to_file('output.txt', 'Washington')"  # noqa
        ],
    )
    additional_properties: Optional[Dict[str, Any]] = None
    additional_output: Optional[StepOutput] = None
    artifacts: List[Artifact] = Field(
        [], description="A list of artifacts that the step has produced."
    )
    is_last: bool = Field(
        ..., description="Whether this is the last step in the task.", examples=[True]
    )


class TaskRequestBody(BaseModel):
    input: Optional[str] = Field(
        None,
        description="Input prompt for the task.",
        examples=["Write 'Washington' to the file 'output.txt'."],
    )
    additional_input: Optional[Dict[str, Any]] = None


class Task(TaskRequestBody):
    task_id: str = Field(
        ...,
        description="The ID of the task.",
        examples=["50da533e-3904-4401-8a07-c49adf88b5eb"],
    )
    steps: List[Step] = Field(..., description="A list of steps that the task has.")
    artifacts: List[Artifact] = Field(
        ...,
        description="A list of artifacts that the task has produced.",
        examples=[
            [
                "7a49f31c-f9c6-4346-a22c-e32bc5af4d8e",
                "ab7b4091-2560-4692-a4fe-d831ea3ca7d6",
            ]
        ],
    )
