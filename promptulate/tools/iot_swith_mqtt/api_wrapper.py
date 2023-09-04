import paho.mqtt.client as mqtt


class IotSwitchAPIWrapper:
    def run(self, client: mqtt, topic: str, command: str) -> str:
        client.publish(topic, command)
        return "ok"
