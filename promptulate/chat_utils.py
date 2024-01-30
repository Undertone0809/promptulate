import json
from typing import Tuple


def parse_content(chunk) -> Tuple[str, str]:
    content = chunk.choices[0].delta.content
    ret_data = json.loads(chunk.json())
    return content, ret_data
