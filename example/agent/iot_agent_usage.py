import paho.mqtt.client as mqtt
from promptulate.agents import ToolAgent
from promptulate.llms import ErnieBot
from promptulate.tools import (
    DuckDuckGoTool,
    Calculator, SleepTool,
)
from promptulate.tools.iot_swith_mqtt import IotSwitchTool
from promptulate.utils.logger import enable_log

enable_log()


def main():
    # MQTT broker address and port
    broker_address = "XXX"
    broker_port = 1883
    # username and password
    username = "XXX"
    password = "XXXXX"
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker_address, broker_port)
    tools = [
        DuckDuckGoTool(),
        Calculator(),
        SleepTool(),
        IotSwitchTool(
            client=client,
            rule_table=[
                {"content": "开冷气", "topic": "/123", "ask": "open fan"},
                {"content": "开加热器", "topic": "/123", "ask": "open heater"},
                {"content": "开灯", "topic": "/123", "ask": "open light"},
            ],
        ),
    ]
    llm = ErnieBot()
    agent = ToolAgent(tools, llm=llm)
    prompt = """我感觉好冷帮我开对应电器，然后暂停3秒后开灯"""
    agent.run(prompt)


if __name__ == "__main__":
    main()
