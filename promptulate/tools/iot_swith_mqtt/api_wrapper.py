class IotSwitchAPIWrapper:
    def run(self, client, topic: str, command: str) -> str:
        client.publish(topic, command)
        return "ok"
