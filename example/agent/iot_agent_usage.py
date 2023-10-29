import paho.mqtt.client as mqtt

from promptulate.agents import ToolAgent
from promptulate.tools import Calculator, DuckDuckGoTool, SleepTool
from promptulate.tools.human_feedback import HumanFeedBackTool
from promptulate.tools.iot_swith_mqtt import IotSwitchTool
from promptulate.utils.logger import enable_log

enable_log()


def main():
    # MQTT broker address and port
    broker_address = "XXX"
    broker_port = 1883
    # username and password
    username = "XXX"
    password = "XXX"
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
    agent = ToolAgent(
        tools,
        enable_role=True,
        agent_name="小创",
        agent_identity="智能音箱",
        agent_goal="控制智能家居，可以开冷气，加热器以及开灯，完成动作后进入闲聊模式",
        agent_constraints="在控制开关电器之前请尽量询问人类",
    )
    prompt = """我现在感觉好暗。"""
    agent.run(prompt)


if __name__ == "__main__":
    main()
