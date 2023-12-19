from importlib.metadata import version

from promptulate.utils.color_print import print_text


def main():
    print_text(
        "🌟 Welcome to Promptulate! Let's create something amazing together!😀", "green"
    )
    print_text(f"Version: {version('promptulate')}", "blue")

    prompt = """Explore the code and contribute on GitHub: 🔗 https://github.com/Undertone0809/promptulate
Access the official documentation: 🔗 https://undertone0809.github.io/promptulate/#/
Need help or have a question? Open an issue: 🔗 https://github.com/Undertone0809/promptulate/issues
Join the development and contribute: 🔗 https://undertone0809.github.io/promptulate/#/other/contribution
    """  # noqa: E501
    print_text(prompt, "blue")


if __name__ == "__main__":
    main()
