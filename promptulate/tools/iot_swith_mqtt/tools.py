import re
from typing import Dict, List

from promptulate.llms import BaseLLM, ChatOpenAI
from promptulate.tools import Tool
from promptulate.tools.iot_swith_mqtt.prompt import prompt_template
from promptulate.utils import StringTemplate


class IotSwitchTool(Tool):
    """A tool for switching operations on various devices"""

    name: str = "Iot_Switch_Mqtt"
    description: str = (
        "An IoT tool used for switching operations on various devices."
        "This tool uses the mqtt protocol for transmission."
        "Args: question(str)"
        "The input content is the intention or command to open the specified electrical appliance."  # noqa
        "If the operation of the device is successful, an OK will be returned, otherwise a failure will be returned."  # noqa
    )
    llm_prompt_template: StringTemplate = prompt_template
    rule_table: List[Dict]

    def __init__(
        self, client, llm: BaseLLM = None, rule_table: List[Dict] = None, **kwargs
    ):
        """
        Args:
            llm(BaseLLM): llm, default is ChatOpenAI
            client(paho.mqtt.client.Client): paho mqtt client which has connected.
            rule_table(List[Dict]):
        """
        self.client = client
        self.llm: BaseLLM = llm or ChatOpenAI(
            temperature=0.1, enable_default_system_prompt=False
        )
        self.rule_table = rule_table

        super().__init__(**kwargs)

    def _run(self, question: str, *args, **kwargs) -> str:
        try:
            import paho.mqtt.client as mqtt  # noqa
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
            topic = self.rule_table[int(answer[0]) - 1]["topic"]
            command = self.rule_table[int(answer[0]) - 1]["ask"]
            self.client.publish(topic, command)
            return "success"
