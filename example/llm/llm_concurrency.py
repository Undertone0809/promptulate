"""
This mode show how to run llm at the same time
"""

from broadcast_service import broadcast_service

from promptulate.llms import OpenAI
from promptulate.utils import set_proxy_mode

counter = 0


@broadcast_service.on_listen("create_llm")
def create_01():
    print("handle 1")
    llm = OpenAI()
    print(llm("给我一段冒泡排序的python代码"))
    global counter
    counter += 1
    print(f"counter {counter}")


@broadcast_service.on_listen("create_llm")
def create_02():
    print("handle 2")
    llm = OpenAI()
    print(llm("给我一段桶排序的python代码"))
    global counter
    counter += 1
    print(f"counter {counter}")


@broadcast_service.on_listen("create_llm")
def create_03():
    llm = OpenAI()
    print(llm("给我一段堆的python代码"))
    global counter
    counter += 1
    print(f"counter {counter}")


@broadcast_service.on_listen("create_llm")
def create_04():
    llm = OpenAI()
    print(llm("给我一段希尔排序的python代码"))
    global counter
    counter += 1
    print(f"counter {counter}")


def main():
    proxies = {"http": "http://127.0.0.1:7890"}
    set_proxy_mode("custom", proxies=proxies)
    broadcast_service.publish("create_llm")
    broadcast_service.publish("create_llm")
    broadcast_service.publish("create_llm")


if __name__ == "__main__":
    main()
