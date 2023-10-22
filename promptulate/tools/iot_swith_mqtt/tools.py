import re
from typing import Dict, List

from promptulate.llms import ChatOpenAI, BaseLLM
from promptulate.tools import Tool
from promptulate.tools.iot_swith_mqtt.api_wrapper import IotSwitchAPIWrapper
from promptulate.tools.iot_swith_mqtt.prompt import prompt_template
from promptulate.utils import StringTemplate, get_logger

logger = get_logger()


class IotSwitchTool(Tool):
    """A tool for switching operations on various devices"""

    name: str = "Iot_Switch_Mqtt"
    description: str = (
        "An IoT tool used for switching operations on various devices."
        "This tool uses the mqtt protocol for transmission."
        "The input content is the intention or command to open the specified electrical appliance."
        "If the operation of the device is successful, an OK will be returned, otherwise a failure will be returned."
    )
    llm_prompt_template: StringTemplate = prompt_template
    rule_table: List[Dict]

    def __init__(
        self,
        client,
        llm: BaseLLM = None,
        rule_table: List[Dict] = None,
        api_wrapper: IotSwitchAPIWrapper = IotSwitchAPIWrapper(),
        **kwargs
    ):
        """
        Args:
            llm: BaseLLM
            client: mqtt.Client
            rule_table: List[Dict]
            api_wrapper: IotSwitchAPIWrapper
        """
        self.api_wrapper = api_wrapper
        self.llm: BaseLLM = llm or ChatOpenAI(
            temperature=0.1, enable_default_system_prompt=False
        )
        self.client = client
        self.rule_table = rule_table

        super().__init__(**kwargs)

    def _run(self, question: str, *args, **kwargs) -> str:
        try:
            import paho.mqtt.client as mqtt
        except ImportError:
            raise ImportError(
                "Could not import paho python package. "
                "This is needed in order to for IotSwitchTool. "
                "Please install it with `pip install paho-mqtt`."
            )
        if len(self.rule_table) == 0:
            raise ValueError("rule_table is empty")
        else:
            index = 1
            key = ""
            for s in self.rule_table:
                key = key + str(index) + "." + s["content"] + "\n"
                index = index + 1
            prompt = self.llm_prompt_template.format(question=question, rule_key=key)
            llm_output = self.llm(prompt)
            return self._process_llm_result(llm_output)

    def _process_llm_result(self, llm_output: str) -> str:
        answer = re.findall(r"\d+", llm_output)
        if len(answer) == 0:
            return "failure information :" + llm_output
        else:
            self.api_wrapper.run(
                self.client,
                self.rule_table[int(answer[0]) - 1]["topic"],
                self.rule_table[int(answer[0]) - 1]["ask"],
            )
            return "ok"
