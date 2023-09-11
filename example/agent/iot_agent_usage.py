import paho.mqtt.client as mqtt
from promptulate.agents import ToolAgent
from promptulate.tools import (
    DuckDuckGoTool,
    Calculator,
    SleepTool,
)
from promptulate.tools.human_feedback import HumanFeedBackTool
from promptulate.tools.iot_swith_mqtt import IotSwitchTool
from promptulate.utils.logger import enable_log

enable_log()


def main():
    # MQTT broker address and port
    broker_address = "xxx"
    broker_port = 1883
    # username and password
    username = "xxx"
    password = "xxx"
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker_address, broker_port)
    tools = [
        DuckDuckGoTool(),
        Calculator(),
        SleepTool(),
        HumanFeedBackTool(),
        IotSwitchTool(
            client=client,
            rule_table=[
                {
                    "content": "开冷气",
                    "topic": "/123",
                    "ask": "Turn on the air conditioner",
                },
                {"content": "开加热器", "topic": "/123", "ask": "Turn on the heater"},
                {"content": "开灯", "topic": "/123", "ask": "Turn on the light"},
            ],
        ),
    ]
    agent = ToolAgent(tools)
    prompt = """现在你是一个智能音箱，你可以控制冷气，加热器和灯的开关，在开关之前请尽量询问人类，我现在感觉好暗。"""
    agent.run(prompt)


if __name__ == "__main__":
    main()
