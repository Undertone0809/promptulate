from promptulate.utils.proxy import set_proxy_mode


def main():
    proxies = {"http": "http://127.0.0.1:7890"}
    set_proxy_mode("custom", proxies)


if __name__ == "__main__":
    main()
