# from unittest import TestCase

# import paho.mqtt.client as mqtt

# from promptulate import enable_log
# from promptulate.tools.iot_swith_mqtt import IotSwitchTool
# from promptulate.tools.iot_swith_mqtt.api_wrapper import IotSwitchAPIWrapper
# from promptulate.utils import get_logger

# enable_log()
# logger = get_logger()


# class TestIotSwitchAPIWrapper(TestCase):
#     def test_run(self):
#         api_wrapper = IotSwitchAPIWrapper()
#         # MQTT broker address and port
#         broker_address = "XXX"
#         broker_port = 1883
#         # username and password
#         username = "cwl"
#         password = "XXXX"
#         client = mqtt.Client()
#         client.username_pw_set(username, password)
#         client.connect(broker_address, broker_port)
#         api_wrapper.run(client, "/123", "hello")


# class TestIotSwitchTool(TestCase):
#     def test_run(self):
#         # MQTT broker address and port
#         broker_address = "XXX"
#         broker_port = 1883
#         # username and password
#         username = "XXXX"
#         password = "XXXXXX"
#         client = mqtt.Client()
#         client.username_pw_set(username, password)
#         client.connect(broker_address, broker_port)
#         tool = IotSwitchTool(
#             client=client,
#             rule_table=[
#                 {"content": "开风扇", "topic": "/123", "ask": "open fan"},
#                 {"content": "开加热器", "topic": "/123", "ask": "open heater"},
#                 {"content": "开灯", "topic": "/123", "ask": "open light"},
#             ],
#         )
#         result = tool.run("我好冷")
#         print(result)
