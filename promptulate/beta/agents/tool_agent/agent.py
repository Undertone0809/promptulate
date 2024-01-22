import time
from typing import Callable, List, Optional, Union

from pydantic import BaseModel, Field

from promptulate.agents.base import BaseAgent
from promptulate.agents.tool_agent.prompt import (
    SYSTEM_PROMPT_TEMPLATE,
)
from promptulate.hook import Hook, HookTable
from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.output_formatter import (
    formatting_result,
    get_formatted_instructions,
)
from promptulate.schema import MessageSet
from promptulate.tools.base import BaseTool, Tool
from promptulate.tools.manager import ToolManager
from promptulate.utils.logger import logger


class ReActResponse(BaseModel):
    thought: str = Field(description="The thought of what to do and why.")
    self_criticism: str = Field(
        description="Constructive self-criticism of the thought"
    )
    tool_name: str = Field(description="The name of tool name.")
    tool_parameters: dict = Field(
        description="The input parameters of tool, string type json parameters."
    )


# Finish tool for ToolAgent
def finish(result: str):
    """Use final answer until you think you have the final answer and can return the
    result.

    Args:
        result: final result content
    """
    return result


def _build_output_format_instruction():
    return get_formatted_instructions(
        json_schema=ReActResponse,
        examples=[
            ReActResponse(
                thought="From the search results, it seems that multiple sources have different weather data formats and information. I will identify the relevant data which is the forecast for tomorrow in Beijing, and then use the finish tool to provide this specific forecast.",  # noqa
                self_criticism="While there is quite a bit of information in the search results, I need to focus on only providing the required weather forecast for tomorrow in Beijing and not get distracted by additional data such as historical weather data or weather for other days.",  # noqa
                tool_name="finish",
                tool_parameters={
                    "result": """In Beijing, the weather forecast for tomorrow is a high of 2\u00b0C and a low of -7\u00b0C.\\"""  # noqa
                },
            )
        ],
    )


class ToolAgent(BaseAgent):
    def __init__(
        self,
        *,
        tools: List[Union[BaseTool, Tool, Callable]],
        llm: Optional[BaseLLM] = None,
        max_iterations: int = 20,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.tool_manager: ToolManager = ToolManager(tools + [finish])
        self.llm: BaseLLM = llm or ChatOpenAI(
            model="gpt-3.5-turbo-16k",
            temperature=0.0,
            enable_default_system_prompt=False,
        )
        self.max_iterations: int = max_iterations
        self.current_iteration: int = 1
        self.max_execution_time: Optional[float] = None
        self.current_time_elapsed: float = 0.0

        self.system_prompt: str = ""
        self.current_process: str = ""
        self.task: str = ""

    def _build_system_prompt(self):
        """ToolAgent use dynamic system prompt. Therefore, this method will be called
        every time before the llm generates a response."""
        self.system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            task=self.task,
            tool_descriptions=self.tool_manager.tool_descriptions,
            current_process=self.current_process,
            output_format=_build_output_format_instruction(),
        )
        logger.info(f"[pne] ToolAgent system prompt: {self.system_prompt}")

    def _build_current_process(self, result: ReActResponse, tool_result: str):
        """Build current process of task."""
        if self.current_process == "":
            self.current_process = """## Current Process of Task
Here is what you have already done. You need to infer what the next task needs to be done based on the previous one.\n"""  # noqa

        self.current_process += f"Step {self.current_iteration}:\n"
        self.current_process += f"Thought: {result.thought}\n"
        self.current_process += f"Self Criticism: {result.self_criticism}\n"
        self.current_process += f"Tool: {result.tool_name}\n"
        self.current_process += f"Tool Parameters: {result.tool_parameters}\n"
        self.current_process += f"Observation: {tool_result}\n\n"
        self.current_process += "---\n"

    def _run(self, task: str, *args, **kwargs) -> str:
        self.task: str = task

        start_time = time.time()

        while self._should_continue():
            self._build_system_prompt()

            messages = MessageSet.from_listdict_data(
                [{"role": "system", "content": self.system_prompt}]
            )
            llm_response: str = self.llm.predict(messages=messages).content
            result: ReActResponse = formatting_result(ReActResponse, llm_response)

            Hook.call_hook(
                HookTable.ON_AGENT_ACTION,
                self,
                thought=f"{result.thought}\n{result.self_criticism}",
                action=result.tool_name,
                action_input=result.tool_parameters,
            )

            if result.tool_name == "finish":
                return result.tool_parameters["result"]

            tool_result: str = self.tool_manager.run_tool(
                result.tool_name, result.tool_parameters
            )
            self._build_current_process(result, tool_result)

            Hook.call_hook(
                HookTable.ON_AGENT_OBSERVATION, self, observation=tool_result
            )

            self.current_iteration += 1
            self.current_time_elapsed += time.time() - start_time

    def _should_continue(self) -> bool:
        """Determine whether to stop, both timeout and exceeding the maximum number of
        iterations will stop.

        Returns:
            Whether to stop.
        """
        if self.current_iteration >= self.max_iterations:
            return False

        if (
            self.max_execution_time
            and self.current_time_elapsed >= self.max_execution_time
        ):
            return False

        return True

    def get_llm(self) -> BaseLLM:
        return self.llm
