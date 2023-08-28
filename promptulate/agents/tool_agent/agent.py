import logging
import re
import time
from abc import abstractmethod, ABC
from typing import List, Callable, Optional

from promptulate.agents.tool_agent.prompt import REACT_ZERO_SHOT_PROMPT
from promptulate.hook import Hook, HookTable
from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.tools import BaseTool
from promptulate.tools.manager import ToolManager
from promptulate.utils.core_utils import generate_run_id
from promptulate.utils.string_template import StringTemplate

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class of Agent."""

    def __init__(self, hooks: List[Callable] = None, *args, **kwargs):
        if hooks:
            for hook in hooks:
                Hook.mount_instance_hook(hook, self)
        Hook.call_hook(HookTable.ON_AGENT_CREATE, self, **kwargs)

    def run(self, *args, **kwargs):
        """run the tool including specified function and hooks"""
        Hook.call_hook(HookTable.ON_AGENT_START, self, *args, **kwargs)
        result: str = self._run(*args, **kwargs)
        Hook.call_hook(HookTable.ON_AGENT_RESULT, self, result=result)
        return result

    @abstractmethod
    def _run(self, *args, **kwargs) -> str:
        """Run the detail agent, implemented by subclass."""


class ToolAgent(BaseAgent):
    """An agent who is good at using tool."""

    def __init__(
        self,
        tools: List[BaseTool],
        llm: BaseLLM = ChatOpenAI(
            model="gpt-3.5-turbo-16k", temperature=0.2, enable_preset_description=False
        ),
        stop_sequences: List[str] = None,
        system_prompt_template: StringTemplate = StringTemplate(REACT_ZERO_SHOT_PROMPT),
        hooks: List[Callable] = None,
    ):
        super().__init__(hooks=hooks)
        self.run_id = generate_run_id()
        self.llm: BaseLLM = llm
        """llm driver"""
        self.stop_sequences: List[str] = stop_sequences
        """llm output will stop when stop sequences is met."""
        self.system_prompt_template: StringTemplate = system_prompt_template
        """Preset system prompt template."""
        self.tool_manager: ToolManager = ToolManager(tools)
        """Used to manage all tools."""
        self.conversation_prompt: str = ""
        """Store all conversation message when conversation."""
        self.max_iterations: Optional[int] = 15
        """The maximum number of executions."""
        self.max_execution_time: Optional[float] = None
        """The longest running time. """

        if not stop_sequences:
            self.stop_sequences = ["Observation"]

    def _build_preset_prompt(self, prompt) -> str:
        """Build the system prompt."""
        return self.system_prompt_template.format(
            prompt=prompt,
            tool_descriptions=self.tool_manager.tool_descriptions,
            tool_names=self.tool_manager.tool_names,
        )

    def _run(self, prompt: str) -> str:
        self.conversation_prompt = self._build_preset_prompt(prompt)
        logger.info(f"[pne] tool agent system prompt: {self.conversation_prompt}")

        iterations = 0
        used_time = 0.0
        start_time = time.time()

        while self._should_continue(iterations, used_time):
            answer = self.llm(prompt=self.conversation_prompt, stop=self.stop_sequences)
            self.conversation_prompt += f"{answer}\n"
            logger.info(
                f"[pne] tool agent <{iterations}> current prompt: {self.conversation_prompt}"
            )

            if "Final Answer" in answer:
                return answer.split("Final Answer:")[-1]

            action, action_input = self._find_action(answer)
            Hook.call_hook(
                HookTable.ON_AGENT_ACTION,
                self,
                action=action,
                action_input=action_input,
            )
            tool_result = self.tool_manager.run_tool(action, action_input)
            Hook.call_hook(HookTable.ON_AGENT_OBSERVATION, self, observation=tool_result)
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
            Return a tuple, (action, action input)
            action(str): tool name
            action_input(str): tool parameters
        """
        action_pattern = r"Action:\s*([\w-]+)"
        action_input_pattern = r"Action Input:\s*(.+)"
        action_match = re.search(action_pattern, answer)
        action_input_match = re.search(action_input_pattern, answer)
        action = None
        action_input = None

        if action_match:
            action = action_match.group(1)
            logger.info(f"[pne] tool agent get Action <{action}>")

        if action_input_match:
            action_input = action_input_match.group(1)
            if action_input.startswith('"'):
                action_input = action_input[1:-1]
            logger.info(f"[pne] tool agent get Action Input <{action_input}>")

        return action, action_input
