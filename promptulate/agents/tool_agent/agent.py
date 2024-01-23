import json
import time
from typing import Callable, List, Optional, Union

from promptulate.agents import BaseAgent
from promptulate.agents.tool_agent.prompt import (
    PREFIX_TEMPLATE,
    REACT_SYSTEM_PROMPT_TEMPLATE,
)
from promptulate.hook import Hook, HookTable
from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.tools.base import BaseTool, Tool
from promptulate.tools.manager import ToolManager
from promptulate.utils.logger import logger
from promptulate.utils.string_template import StringTemplate


class ToolAgent(BaseAgent):
    """
    An agent who is good at using tool. ref ReAct.

    Attributes:
        llm (BaseLLM): The language model driver. Default is ChatOpenAI with model
            "gpt-3.5-turbo-16k".
        stop_sequences (List[str]): The sequences that, when met, will stop the output
            of the llm.
        system_prompt_template (StringTemplate): The preset system prompt template.
        prefix_prompt_template (StringTemplate): The prefix system prompt template.
        tool_manager (ToolManager): Used to manage all tools.
        conversation_prompt (str): Stores all conversation messages during a
            conversation.
        max_iterations (Optional[int]): The maximum number of executions. Default is 15.
        max_execution_time (Optional[float]): The longest running time. No default
            value.
        enable_role (bool): Flag to enable role. Default is False.
        agent_name (str): The name of the agent. Default is "pne-bot".
        agent_identity (str): The identity of the agent. Default is "bot".
        agent_goal (str): The goal of the agent. Default is "provides better assistance
            and services for humans.".
        agent_constraints (str): The constraints of the agent. Default is "none".
    """

    def __init__(
        self,
        *,
        tools: List[Union[BaseTool, Tool, Callable]],
        llm: BaseLLM = None,
        stop_sequences: List[str] = None,
        prefix_prompt_template: StringTemplate = StringTemplate(PREFIX_TEMPLATE),
        hooks: List[Callable] = None,
        enable_role: bool = False,
        agent_name: str = "tool-agent",
        agent_identity: str = "tool-agent",
        agent_goal: str = "provides better assistance and services for humans.",
        agent_constraints: str = "none",
    ):
        super().__init__(hooks=hooks)
        self.llm: BaseLLM = llm or ChatOpenAI(
            model="gpt-3.5-turbo-16k",
            temperature=0.0,
            enable_default_system_prompt=False,
        )
        """llm provider"""
        self.tool_manager: ToolManager = ToolManager(tools)
        """Used to manage all tools."""
        self.stop_sequences: List[str] = stop_sequences
        """llm output will stop when stop sequences is met."""
        self.system_prompt_template: StringTemplate = REACT_SYSTEM_PROMPT_TEMPLATE
        """Preset system prompt template."""
        self.prefix_prompt_template: StringTemplate = prefix_prompt_template
        """Prefix system prompt template."""
        self.conversation_prompt: str = ""
        """Store all conversation message when conversation. ToolAgent use dynamic
        system prompt."""
        self.max_iterations: Optional[int] = 15
        """The maximum number of executions."""
        self.max_execution_time: Optional[float] = None
        """The longest running time. """
        self.enable_role: bool = enable_role
        self.agent_name: str = agent_name
        self.agent_identity: str = agent_identity
        self.agent_goal: str = agent_goal
        self.agent_constraints: str = agent_constraints
        self.stop_sequences = stop_sequences or ["Observation"]

    def get_llm(self) -> BaseLLM:
        return self.llm

    def _build_system_prompt(self, instruction: str) -> str:
        """Build the system prompt."""
        prefix_prompt = (
            self.prefix_prompt_template.format(
                agent_identity=self.agent_identity,
                agent_name=self.agent_name,
                agent_goal=self.agent_goal,
                agent_constraints=self.agent_constraints,
            )
            if self.enable_role
            else ""
        )

        return prefix_prompt + self.system_prompt_template.format(
            question=instruction,
            tool_descriptions=self.tool_manager.tool_descriptions,
        )

    def _run(self, instruction: str, *args, **kwargs) -> str:
        self.conversation_prompt = self._build_system_prompt(instruction)
        logger.info(f"[pne] ToolAgent system prompt: {self.conversation_prompt}")

        iterations = 0
        used_time = 0.0
        start_time = time.time()

        while self._should_continue(iterations, used_time):
            llm_resp: str = self.llm(
                instruction=self.conversation_prompt, stop=self.stop_sequences
            )
            while llm_resp == "":
                llm_resp = self.llm(
                    instruction=self.conversation_prompt, stop=self.stop_sequences
                )

            thought, action_name, action_parameters = self._parse_llm_response(llm_resp)
            self.conversation_prompt += f"{llm_resp}\n"
            logger.info(
                f"[pne] tool agent <{iterations}> current prompt: {self.conversation_prompt}"  # noqa
            )

            if "finish" in action_name:
                return action_parameters["content"]

            Hook.call_hook(
                HookTable.ON_AGENT_ACTION,
                self,
                thought=thought,
                action=action_name,
                action_input=action_parameters,
            )

            tool_result = self.tool_manager.run_tool(action_name, action_parameters)
            Hook.call_hook(
                HookTable.ON_AGENT_OBSERVATION, self, observation=tool_result
            )
            self.conversation_prompt += f"Observation: {tool_result}\n"

            iterations += 1
            used_time += time.time() - start_time

    def _should_continue(self, current_iteration: int, current_time_elapsed) -> bool:
        """Determine whether to stop, both timeout and exceeding the maximum number of
        iterations will stop.

        Args:
            current_iteration: current iteration times.
            current_time_elapsed: current running time.

        Returns:
            Whether to stop.
        """
        if self.max_iterations and current_iteration >= self.max_iterations:
            return False
        if self.max_execution_time and current_time_elapsed >= self.max_execution_time:
            return False
        return True

    def _parse_llm_response(self, llm_resp: str) -> (str, str, Union[dict, str]):
        """Parse next instruction of LLM output.

        Args:
            llm_resp(str): output of LLM

        Returns:
            Return a tuple, (thought,action,action input)
            action(str): tool name
            action_input(dict | str): tool parameters
        """
        llm_resp: str = (
            llm_resp.replace("```json", "").replace("```JSON", "").replace("```", "")
        )
        data: dict = json.loads(llm_resp)

        return data["thought"], data["action"]["name"], data["action"]["args"]
