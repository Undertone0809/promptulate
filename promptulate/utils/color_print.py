from typing import Optional

from typing_extensions import Literal

COLOR_MAPPING = {
    "blue": "36;1",
    "yellow": "33;1",
    "pink": "38;5;200",
    "green": "32;1",
    "red": "31;1",
}
COLOR_TYPE = Literal["blue", "yellow", "pink", "green", "red"]


def print_text(text: str, color: Optional[COLOR_TYPE] = None):
    if not color:
        print(text)
        return

    if color not in COLOR_MAPPING:
        ValueError("Wrong color, only blue, yellow, pink, green, red can be used.")
    print(f"\u001b[{COLOR_MAPPING[color]}m\033[1;3m{text}\u001b[0m")
