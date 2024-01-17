import paho.mqtt.client as mqtt

from promptulate.agents import ToolAgent
from promptulate.tools import Calculator, DuckDuckGoTool, sleep_tool
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
        sleep_tool,
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
        tools=tools,
        enable_role=True,
        agent_name="xiao chang",
        agent_identity="Smart speaker.",
        agent_goal="Control smart home, can turn on the "
        "air conditioner, heater, and lights, and enter into chat mode "
        "after completing the action.",
        agent_constraints="Please try to ask humans before controlling "
        "or switching on electrical appliances.",
    )
    prompt = """I feel so dark now."""
    agent.run(prompt)


if __name__ == "__main__":
    main()
