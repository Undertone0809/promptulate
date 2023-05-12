# -*- coding: utf-8 -*-
# @Time    : 2023/5/11 22:03
# @Author  : Zeeland
# @File    : test.py
# @Software: PyCharm
from promptulate.schema import ChatMessageHistory, UserMessage, SystemMessage

c = ChatMessageHistory()
c.add_system_message("只因你太美")
c.add_user_message("只因你实在是太美")

print(c.to_local_cache_form())
