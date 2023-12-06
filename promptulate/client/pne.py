from importlib.metadata import version

from promptulate.utils.color_print import print_text


def main():
    print_text("🌟 Welcome to Promptulate! 😀", "green")
    print_text(f"Version: {version('promptulate')}", "blue")
    print_text("Github repo: https://github.com/Undertone0809/promptulate", "blue")
    print_text(
        "Official document: https://undertone0809.github.io/promptulate/#/", "blue"
    )


if __name__ == "__main__":
    main()
