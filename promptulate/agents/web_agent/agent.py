from typing import Callable, List

from promptulate.agents import BaseAgent
from promptulate.agents.web_agent.prompt import SYSTEM_PROMPT_TEMPLATE
from promptulate.hook import Hook, HookTable
from promptulate.llms import BaseLLM, ChatOpenAI, ErnieBot
from promptulate.tools import DuckDuckGoTool
from promptulate.utils.logger import logger


def _build_system_prompt(prompt) -> str:
    """Build the system prompt."""
    return SYSTEM_PROMPT_TEMPLATE.format(prompt=prompt)


class WebAgent(BaseAgent):
    def __init__(
        self,
        llm: BaseLLM = None,
        hooks: List[Callable] = None,
        *args,
        **kwargs,
    ):
        super().__init__(hooks, *args, **kwargs)
        self.llm: BaseLLM = llm or ChatOpenAI(
            model="gpt-3.5-turbo-16k",
            temperature=0.0,
            enable_default_system_prompt=False,
        )
        self.stop_sequences: List[str] = ["Observation"]
        self.websearch = DuckDuckGoTool()
        self.conversation_prompt: str = ""

    def get_llm(self) -> BaseLLM:
        return self.llm

    def _run(self, prompt: str, *args, **kwargs) -> str:
        # ErnieBot built-in network search
        if self.llm.llm_type == "ErnieBot":
            self.llm = ErnieBot(
                model=self.llm.model, temperature=0.1, disable_search=False
            )
            return self.llm(prompt)

        self.conversation_prompt = _build_system_prompt(prompt)
        iterations = 0

        # Loop search until find the answer
        while True:
            llm_output: str = self.llm(
                self.conversation_prompt, stop=self.stop_sequences
            )
            logger.info(
                f"[pne] tool agent <{iterations}> current prompt: {self.conversation_prompt}"  # noqa
            )

            if "Final Answer" in llm_output:
                return llm_output.split("Final Answer:")[-1]

            self.conversation_prompt += llm_output

            # get keywords and query by websearch
            query_words: str = self._find_query_words(llm_output)
            Hook.call_hook(
                HookTable.ON_AGENT_ACTION,
                self,
                action="websearch",
                action_input=query_words,
                thought=llm_output.split("\n")[0],
            )

            query_result: str = self.websearch.run(query_words)
            Hook.call_hook(
                HookTable.ON_AGENT_OBSERVATION, self, observation=query_result
            )

            self.conversation_prompt += f"Observation: {query_result}\nThought: "
            iterations += 1

    def _find_query_words(self, answer: str) -> str:
        return answer.split("Query:")[-1].replace('"', "")
