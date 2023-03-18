# CushyChat
一个测试ChatGPT API的简易聊天机器人。支持连续对话，提供缓存的功能，可以记录历史对话，但是相关功能还懒得开发。

# 快速上手

```shell script
pip install -r requirements.txt
```

- 将`cushy-chat.py`中的`API_KEY`修改为自己的KEY

- 直接运行`cushy-chat.py`即可

# TODO
- 读取历史消息（已经提供缓存）
- 选取历史消息进行长对话聊天
- 提供token长度判断功能


# 参考

- 好人一生平安
- 感谢 [ayaka14732](https://github.com/ayaka14732) 提供的API代理 [https://github.com/ayaka14732/ChatGPTAPIFree/](https://github.com/ayaka14732/ChatGPTAPIFree/blob/main/README-zh_CN.md) 
- OpenAI API [https://platform.openai.com/docs/api-reference/chat/create](https://platform.openai.com/docs/api-reference/chat/create)
- OpenAI API [https://platform.openai.com/docs/guides/chat/instructing-chat-models](https://platform.openai.com/docs/guides/chat/instructing-chat-models)