import re
from typing import Optional, Dict, List

from pydantic import Field

from promptulate.llms import ErnieBot, BaseLLM
from promptulate.tools import BaseTool
from promptulate.tools.iot_swith_mqtt.api_wrapper import IotSwitchAPIWrapper
import paho.mqtt.client as mqtt

from promptulate.tools.iot_swith_mqtt.prompt import prompt_template
from promptulate.utils import StringTemplate, get_logger

logger = get_logger()


class IotSwitchTool(BaseTool):
    """A tool for running python code in a REPL."""

    name: str = "Iot_Switch_Mqtt"
    description: str = (
        "An IoT tool used for switching operations on various devices"
        "This tool uses the mqtt protocol for transmission"
        "The input content is the intention or command to open the specified electrical appliance"
        "If the operation of the device is successful, an OK will be returned, otherwise a failure will be returned"
    )
    llm_prompt_template: StringTemplate = Field(default=prompt_template)
    llm: BaseLLM = Field(
        default=ErnieBot(temperature=0.3)
    )
    client: mqtt.Client
    rule_table: List[Dict]
    api_wrapper: IotSwitchAPIWrapper = Field(default_factory=IotSwitchAPIWrapper)

    def _run(self, question: str, *args, **kwargs) -> str:
        if len(self.rule_table) == 0:
            raise Exception("rule_table is empty")
        else:
            index = 1
            key = ""
            for s in self.rule_table:
                key = key+str(index) + "." + s["content"] + "\n"
                index = index + 1
            prompt = self.llm_prompt_template.format(question=question, rule_key=key)
            logger.debug(prompt)
            llm_output = self.llm(prompt)
            return self._process_llm_result(llm_output)

    def _process_llm_result(self, llm_output: str) -> str:
        answer = re.findall(r"\d+", llm_output)
        if len(answer) == 0:
            return "failure information :"+llm_output
        else:
            self.api_wrapper.run(
                self.client,
                self.rule_table[int(answer[0]) - 1]["topic"],
                self.rule_table[int(answer[0]) - 1]["ask"],
            )
            return "ok"
