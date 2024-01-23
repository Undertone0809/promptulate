from promptulate.agents.tool_agent.agent import ToolAgent
from promptulate.llms.base import BaseLLM
from promptulate.tools.duckduckgo.tools import ddg_websearch


class WebAgent(ToolAgent):
    def __init__(self, llm: BaseLLM = None, *args, **kwargs):
        super().__init__(tools=[ddg_websearch], llm=llm, *args, **kwargs)
