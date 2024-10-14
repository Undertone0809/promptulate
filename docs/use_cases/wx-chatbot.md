# WeChat Chatbot

## Overview

This code implements a WeChat chatbot that interacts with WeChat using the `itchat` library and generates replies using OpenAI's GPT-3.5-turbo model. The bot can receive text messages and process them accordingly.

## Main Features

1. **Message Handling**: Receives text messages from WeChat and generates replies using the GPT-3.5-turbo model.
2. **QR Code Login**: Generates a QR code for users to scan and log in to WeChat.
3. **Error Handling**: Captures and logs exceptions during message processing.

## Code Structure

### 1. Import Necessary Libraries

```python
import time
import chat_message
import itchat
import pne
from itchat.content import TEXT
from itchat.storage.messagequeue import Message
from promptulate.utils import logger
```

- `time`: Used to control the program's runtime.
- `chat_message`: A custom module for handling chat messages.
- `itchat`: Used for interacting with WeChat.
- `pne`: Used to call OpenAI's chat interface.
- `logger`: Used for logging.

### 2. Message Handling Function

```python
@itchat.msg_register([TEXT])
def handler_single_msg(msg: Message):
    ...
```

- This function is registered as a message handler, receiving text messages and calling the `handle` method of the `MessageHandler` class for processing.

### 3. QR Code Callback Function

```python
def qrCallback(uuid, status, qrcode):
    ...
```

- This function is called after the QR code is generated, providing multiple QR code links for the user to scan and log in.

### 4. Startup Function

```python
def startup():
    ...
```

- This function initializes `itchat`, logs in to WeChat, and starts receiving messages.

### 5. Message Handling Class

```python
class MessageHandler:
    ...
```

- This class is responsible for processing received messages and generating replies using OpenAI's API.

### 6. Main Program Entry

```python
if __name__ == "__main__":
    startup()
    while True:
        time.sleep(1)
```

- The main entry point of the program, calling the `startup` function and keeping the program running.

## Usage Instructions

1. **Install Dependencies**:
   Ensure that the `itchat` and `pne` libraries are installed. You can use the following command:

   ```bash
   pip install itchat pne
   ```

2. **Configure API Key**:
   In the `MessageHandler` class, replace `api_key` with your OpenAI API key.

3. **Run the Program**:
   Execute the `app.py` file, and the program will generate a QR code for the user to scan and log in.

4. **Send Messages**:
   After logging in, users can send text messages, and the bot will automatically reply.

## Notes

- Ensure a stable internet connection to access OpenAI's API.
- Be cautious when handling sensitive information, such as protecting the API key and user data.


