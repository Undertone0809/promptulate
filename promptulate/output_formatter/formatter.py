import json
import re
from typing import TypeVar, List, Dict

from pydantic import BaseModel

from promptulate.output_formatter.prompt import OUTPUT_FORMAT
from promptulate.tips import OutputParserError

T = TypeVar("T", bound=BaseModel)


def _get_schema(pydantic_obj: type(BaseModel)) -> Dict:
    """Get reduced schema from pydantic object."""

    # Remove useless fields.
    reduced_schema = pydantic_obj.schema()
    if "title" in reduced_schema:
        del reduced_schema["title"]
    if "type" in reduced_schema:
        del reduced_schema["type"]
    for k, v in reduced_schema["properties"].items():
        if "title" in v:
            del v["title"]

    return reduced_schema


class OutputFormatter:
    def __init__(self, pydantic_obj: type(BaseModel), examples: List[BaseModel] = None):
        self.pydantic_obj = pydantic_obj
        self.examples = examples

    def get_formatted_instructions(self) -> str:
        return get_formatted_instructions(self.pydantic_obj, self.examples)

    def formatting_result(self, llm_output: str) -> T:
        return formatting_result(self.pydantic_obj, llm_output)

def get_formatted_instructions(
    pydantic_obj: type(BaseModel), examples: List[BaseModel] = None
) -> str:
    # Ensure json with double quotes.
    schema_str = json.dumps(_get_schema(pydantic_obj))

    instructions: str = OUTPUT_FORMAT.format(schema=schema_str)
    if examples:
        instructions += "\nExamples:\n"
        for example in examples:
            example_str = json.dumps(example.dict())
            instructions += f"{example_str}\n"
    return instructions


def formatting_result(pydantic_obj: type(BaseModel), llm_output: str) -> T:
    """Parse llm_output and instantiate the result as provided pydantic_obj."""
    try:
        match = re.search(
            r"\{.*\}", llm_output.strip(), re.MULTILINE | re.IGNORECASE | re.DOTALL
        )
        json_str = match.group() if match else ""
        json_object = json.loads(json_str, strict=False)
        return pydantic_obj.parse_obj(json_object)
    except Exception as e:
        name = pydantic_obj.__name__
        msg = f"Failed to parse {name} from completion {llm_output}. Got: {e}"
        raise OutputParserError(msg, llm_output)
