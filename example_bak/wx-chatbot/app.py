import time

import chat_message
import itchat
import pne
from itchat.content import TEXT
from itchat.storage.messagequeue import Message

from promptulate.utils import logger


@itchat.msg_register([TEXT])
def handler_single_msg(msg: Message):
    try:
        print(msg)
        print("Get a new messsage: {}".format(msg.Content))
        handler.handle(chat_message.ReceiveMessage(msg))
    except NotImplementedError as e:
        logger.debug("[WX]single message {} skipped: {}".format(msg["MsgId"], e))
        return None
    return None


def qrCallback(uuid, status, qrcode):
    # logger.debug("qrCallback: {} {}".format(uuid,status))
    if status == "0":
        url = f"https://login.weixin.qq.com/l/{uuid}"

        qr_api1 = "https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}".format(url)
        qr_api2 = (
            "https://api.qrserver.com/v1/create-qr-code/?size=400×400&data={}".format(
                url
            )
        )
        qr_api3 = "https://api.pwmqr.com/qrcode/create/?url={}".format(url)
        qr_api4 = "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}".format(
            url
        )
        print("You can also scan QRCode in any website below:")
        print(qr_api3)
        print(qr_api4)
        print(qr_api2)
        print(qr_api1)


def startup():
    try:
        # itchat.instance.receivingRetryCount = 600  # 修改断线超时时间
        hotReload = False
        itchat.auto_login(
            enableCmdQR=2,
            hotReload=hotReload,
            qrCallback=qrCallback,
        )
        user_id = itchat.instance.storageClass.userName
        name = itchat.instance.storageClass.nickName
        logger.info(
            "Wechat login success, user_id: {}, nickname: {}".format(user_id, name)
        )  # noqa: E501
        itchat.run()
    except Exception as e:
        logger.exception(e)


class MessageHandler:
    def __init__(self):
        pass

    def handle(self, msg: chat_message.ReceiveMessage):
        receiver = msg.FromUserName
        response = pne.chat(
            messages=msg.Content,
            model="gpt-3.5-turbo",
            model_config={
                "api_key": "sk-xxxxxx",
                "base_url": "https://api.openai.com/v1",
            },
        )
        itchat.send(response.result, toUserName=receiver)


handler = MessageHandler()


if __name__ == "__main__":
    startup()
    while True:
        time.sleep(1)
