import logging
import re
import time
from typing import Callable, List, Optional, Union

from promptulate.agents import BaseAgent
from promptulate.agents.tool_agent.prompt import PREFIX_TEMPLATE, REACT_ZERO_SHOT_PROMPT
from promptulate.hook import Hook, HookTable
from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.tools.base import BaseTool, Tool
from promptulate.tools.manager import ToolManager
from promptulate.utils.string_template import StringTemplate

logger = logging.getLogger(__name__)


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
        tools: List[Union[BaseTool, Tool]],
        llm: BaseLLM = None,
        stop_sequences: List[str] = None,
        prefix_prompt_template: StringTemplate = StringTemplate(PREFIX_TEMPLATE),
        system_prompt_template: StringTemplate = StringTemplate(REACT_ZERO_SHOT_PROMPT),
        hooks: List[Callable] = None,
        enable_role: bool = False,
        agent_name: str = "pne-bot",
        agent_identity: str = "bot",
        agent_goal: str = "provides better assistance and services for humans.",
        agent_constraints: str = "none",
    ):
        super().__init__(hooks=hooks)
        self.llm: BaseLLM = llm or ChatOpenAI(
            model="gpt-3.5-turbo-16k",
            temperature=0.2,
            enable_default_system_prompt=False,
        )
        """llm driver"""
        self.stop_sequences: List[str] = stop_sequences
        """llm output will stop when stop sequences is met."""
        self.system_prompt_template: StringTemplate = system_prompt_template
        """Preset system prompt template."""
        self.prefix_prompt_template: StringTemplate = prefix_prompt_template
        """Prefix system prompt template."""
        self.tool_manager: ToolManager = ToolManager(tools)
        """Used to manage all tools."""
        self.conversation_prompt: str = ""
        """Store all conversation message when conversation."""
        self.max_iterations: Optional[int] = 15
        """The maximum number of executions."""
        self.max_execution_time: Optional[float] = None
        """The longest running time. """
        self.enable_role: bool = enable_role
        self.agent_name: str = agent_name
        self.agent_identity: str = agent_identity
        self.agent_goal: str = agent_goal
        self.agent_constraints: str = agent_constraints
        if not stop_sequences:
            self.stop_sequences = ["Observation"]

    def get_llm(self) -> BaseLLM:
        return self.llm

    def _build_system_prompt(self, prompt) -> str:
        """Build the system prompt."""
        prefix = (
            self.prefix_prompt_template.format(
                agent_identity=self.agent_identity,
                agent_name=self.agent_name,
                agent_goal=self.agent_goal,
                agent_constraints=self.agent_constraints,
            )
            if self.enable_role
            else ""
        )

        return prefix + self.system_prompt_template.format(
            prompt=prompt,
            tool_descriptions=self.tool_manager.tool_descriptions,
            tool_names=self.tool_manager.tool_names,
        )

    def _run(self, prompt: str, *args, **kwargs) -> str:
        self.conversation_prompt = self._build_system_prompt(prompt)
        logger.info(f"[pne] tool agent system prompt: {self.conversation_prompt}")

        iterations = 0
        used_time = 0.0
        start_time = time.time()

        while self._should_continue(iterations, used_time):
            answer = self.llm(prompt=self.conversation_prompt, stop=self.stop_sequences)
            while answer == "":
                answer = self.llm(
                    prompt=self.conversation_prompt, stop=self.stop_sequences
                )
            self.conversation_prompt += f"{answer}\n"
            logger.info(
                f"[pne] tool agent <{iterations}> current prompt: {self.conversation_prompt}"  # noqa
            )

            if "Final Answer" in answer:
                return answer.split("Final Answer:")[-1]

            action, thought, action_input = self._find_action(answer)
            Hook.call_hook(
                HookTable.ON_AGENT_ACTION,
                self,
                action=action,
                thought=thought,
                action_input=action_input,
            )
            tool_result = self.tool_manager.run_tool(action, action_input)
            Hook.call_hook(
                HookTable.ON_AGENT_OBSERVATION, self, observation=tool_result
            )
            self.conversation_prompt += f"Observation: {tool_result}\nThought: "

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

    def _find_action(self, answer: str) -> (str, str):
        """Parse next instruction of LLM output.

        Args:
            answer(str): output of LLM

        Returns:
            Return a tuple, (action,thought, action input)
            action(str): tool name
            action_input(str): tool parameters
        """
        action_pattern = r"Action:\s*([\w-]+)"
        thought_pattern = r"Thought:\s*([\w-]+)"
        action_input_pattern = r"Action Input:\s*(.+)"
        action_match = re.search(action_pattern, answer)
        thought_match = re.search(thought_pattern, answer)
        action_input_match = re.search(action_input_pattern, answer)
        action: str = ""
        thought: str = ""
        action_input: str = ""

        if action_match:
            action = action_match.group(1)
            logger.info(f"[pne] tool agent get Action <{action}>")
        if thought_match:
            thought = thought_match.group(1)
            logger.info(f"[pne] tool agent get Thought <{thought}>")
        if action_input_match:
            action_input = action_input_match.group(1)
            if action_input.startswith('"'):
                action_input = action_input[1:-1]
            logger.info(f"[pne] tool agent get Action Input <{action_input}>")

        return action, thought, action_input
