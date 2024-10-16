# Building a WeChat Chatbot with Pne and ItChat

This guide will walk you through the steps to create a basic WeChat chatbot using the Pne framework, an AI agent tool, and the ItChat library for handling WeChat messages. By following this tutorial, even beginners can build a chatbot from scratch.

#### Prerequisites

Before starting, ensure you have the following installed:

- Python 3.x
- Basic understanding of Python
- A WeChat account
- The following Python packages:
  - itchat
  - pne
  - promptulate

You can install the necessary packages by running:

```bash
pip install -r requirements.txt
```

### Step 1: Import Necessary Libraries

To get started, import the required libraries:

```python
import time
import chat_message  # custom module for handling chat messages
import itchat        # WeChat interaction library
import pne           # Pne framework for AI-driven message handling
from itchat.content import TEXT
from itchat.storage.messagequeue import Message
from promptulate.utils import logger
```

### Step 2: Define the Message Handler

We use itchat.msg_register to define how the bot will respond to text messages. This method registers the message handler for incoming messages:

```python
@itchat.msg_register([TEXT])
def handler_single_msg(msg: Message):
    try:
        print("Get a new message: {}".format(msg.Content))
        handler.handle(chat_message.ReceiveMessage(msg))
    except NotImplementedError as e:
        logger.debug("[WX] single message {} skipped: {}".format(msg["MsgId"], e))
        return None
    return None
```

This function:

- Logs the message content
- Uses a handler (which we define later) to process the incoming message and generate a response
- Handles potential exceptions with logging

### Step 3: Generate a QR Code for WeChat Login

WeChat login requires scanning a QR code. Here, we provide several QR code generation options:

```python
def qrCallback(uuid, status, qrcode):
    if status == "0":
        url = f"https://login.weixin.qq.com/l/{uuid}"

        qr_api1 = "https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}".format(url)
        qr_api2 = (
            "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={}".format(url)
        )
        qr_api3 = "https://api.pwmqr.com/qrcode/create/?url={}".format(url)
        qr_api4 = "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}".format(url)

        print("You can scan the QRCode on one of these websites:")
        print(qr_api3)
        print(qr_api4)
        print(qr_api2)
        print(qr_api1)
```

This function generates multiple QR codes from different services, allowing the user to scan one for WeChat login.

### Building a WeChat Chatbot with Pne and ItChat

This guide will walk you through the steps to create a basic WeChat chatbot using the Pne framework, an AI agent tool, and the ItChat library for handling WeChat messages. By following this tutorial, even beginners can build a chatbot from scratch.

Prerequisites

Before starting, ensure you have the following installed:

    •	Python 3.x
    •	Basic understanding of Python
    •	A WeChat account
    •	The following Python packages:
    •	itchat
    •	pne
    •	promptulate

You can install the necessary packages by running:

pip install itchat pne promptulate

Step 1: Import Necessary Libraries

To get started, import the required libraries:

import time
import chat_message # custom module for handling chat messages
import itchat # WeChat interaction library
import pne # Pne framework for AI-driven message handling
from itchat.content import TEXT
from itchat.storage.messagequeue import Message
from promptulate.utils import logger

Step 2: Define the Message Handler

We use itchat.msg_register to define how the bot will respond to text messages. This method registers the message handler for incoming messages:

@itchat.msg_register([TEXT])
def handler_single_msg(msg: Message):
try:
print("Get a new message: {}".format(msg.Content))
handler.handle(chat_message.ReceiveMessage(msg))
except NotImplementedError as e:
logger.debug("[WX] single message {} skipped: {}".format(msg["MsgId"], e))
return None
return None

This function:

    •	Logs the message content
    •	Uses a handler (which we define later) to process the incoming message and generate a response
    •	Handles potential exceptions with logging

Step 3: Generate a QR Code for WeChat Login

WeChat login requires scanning a QR code. Here, we provide several QR code generation options:

def qrCallback(uuid, status, qrcode):
if status == "0":
url = f"https://login.weixin.qq.com/l/{uuid}"

        qr_api1 = "https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}".format(url)
        qr_api2 = (
            "https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={}".format(url)
        )
        qr_api3 = "https://api.pwmqr.com/qrcode/create/?url={}".format(url)
        qr_api4 = "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}".format(url)

        print("You can scan the QRCode on one of these websites:")
        print(qr_api3)
        print(qr_api4)
        print(qr_api2)
        print(qr_api1)

This function generates multiple QR codes from different services, allowing the user to scan one for WeChat login.

### Step 4: Initialize and Run the Chatbot

The startup() function initializes the WeChat login process and begins listening for messages:

```python
def startup():
    try:
        itchat.auto_login(
            enableCmdQR=2,
            hotReload=False,   # Set to True to avoid logging in every time
            qrCallback=qrCallback
        )
        user_id = itchat.instance.storageClass.userName
        name = itchat.instance.storageClass.nickName
        logger.info(
            "WeChat login success, user_id: {}, nickname: {}".format(user_id, name)
        )
        itchat.run()
    except Exception as e:
        logger.exception(e)
```

### Step 5: Define the AI Response Logic

Here’s where we leverage Pne to generate AI-driven responses using the GPT-3.5 model. When a message is received, Pne processes it and returns a response that is sent back to the user.

```python
class MessageHandler:
    def __init__(self):
        pass

    def handle(self, msg: chat_message.ReceiveMessage):
        receiver = msg.FromUserName
        response = pne.chat(
            messages=msg.Content,
            model="gpt-3.5-turbo",
            model_config={
                "api_key": "sk-xxxxxx",  # Replace with your API key
                "base_url": "https://api.openai.com/v1",
            },
        )
        itchat.send(response.result, toUserName=receiver)

handler = MessageHandler()
```

This class processes incoming messages and sends the AI-generated responses back to the user via WeChat.

### Step 6: Main Loop to Keep the Bot Running

Finally, to ensure the bot runs continuously, we keep the process alive in a loop:

```python
if __name__ == "__main__":
    startup()  # Log into WeChat
    while True:
        time.sleep(1)  # Keep the program running
```

### Running the Chatbot

To run the bot, simply execute the script in your terminal:

```bash
python app.py
```

After running the script, a QR code will be generated. Scan it with WeChat to log in, and your bot will start receiving and responding to messages!

This simple chatbot example shows how to integrate the Pne framework for AI-generated responses and the ItChat library for handling WeChat messages. You can further enhance the bot by implementing more sophisticated message handling, custom responses, and integrating other APIs.
