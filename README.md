# prompt-me

prompt-me是一个由OpenAI GPT API封装而成的轻量级聊天机器人，支持连续对话，提供缓存的功能，可以记录历史对话等功能，开箱即用。

# 特性

- 封装接口，开箱即用
- 内置API代理，不用科学上网也可以直接使用
- 支持调用ChatGPT API官方接口或自治代理
- 支持长对话聊天，聊天记录使用`cushy-storage`进行持久化
- 支持markdowm对话导出

# 快速上手

```shell script
pip install prompt-me --upgrade 
```

- 基本使用

```python
from prompt_me import ChatBot, enable_log


def main():
    # enable_log() # 日志功能
    print("A Simple ChatBot built by ChatGPT API")
    conversation_id = None
    while True:
        prompt = str(input("[User] "))
        bot = ChatBot(key='yourkey')
        ret, conversation_id = bot.ask(prompt, conversation_id)
        print(ret, conversation_id)


if __name__ == '__main__':
    main()
```

- 获取历史对话

```python
from prompt_me import ChatBot, enable_log_no_file


def main():
    # enable_log_no_file()
    bot = ChatBot(key='yourkey')
    ret, conversation_id = bot.ask("please give me a bucket sort python code")
    messages = bot.get_history(conversation_id)
    for message in messages:
        print(message)


if __name__ == '__main__':
    main()
```

- 导出历史对话为markdown

```python
from prompt_me import ChatBot, enable_log_no_file


def main():
    # enable_log_no_file()
    bot = ChatBot(key='yourkey')
    ret, conversation_id = bot.ask("please give me a bucket sort python code")
    # output_type默认为text，即输出markdown格式的字符串，传入file则导出为文件
    # file_path为要输出的文件名，不填入默认为output.md
    output_str = bot.output(conversation_id, output_type='file', file_path='output.md')
    print(output_str)


if __name__ == '__main__':
    main()

```


# TODO

- ~~可以导出历史消息为markdown格式~~
- 提供显示当前token（单词量）的功能
- ~~添加错误处理机制，如网络异常、服务器异常等，保证程序的可靠性~~
- 支持由终端直接输入key进行存储
- ~~开发ChatBot v2, [issue](https://github.com/Undertone0809/cushy-chat/issues/1)~~

# 参考

- 好人一生平安
- 感谢 [ayaka14732](https://github.com/ayaka14732)
  提供的API代理 [https://github.com/ayaka14732/ChatGPTAPIFree/](https://github.com/ayaka14732/ChatGPTAPIFree/blob/main/README-zh_CN.md)
- OpenAI
  API [https://platform.openai.com/docs/api-reference/chat/create](https://platform.openai.com/docs/api-reference/chat/create)
- OpenAI
  API [https://platform.openai.com/docs/guides/chat/instructing-chat-models](https://platform.openai.com/docs/guides/chat/instructing-chat-models)