import json
import re
from typing import TypeVar

from pydantic import BaseModel

from promptulate.output_formatter.prompt import OUTPUT_FORMAT
from promptulate.tips import OutputParserError

T = TypeVar("T", bound=BaseModel)


class OutputFormatter:
    def __init__(self, pydantic_obj: type(BaseModel)):
        self.pydantic_obj = pydantic_obj

    def get_formatted_instructions(self) -> str:
        schema = self.pydantic_obj.schema()

        # Remove useless fields.
        reduced_schema = schema
        if "title" in reduced_schema:
            del reduced_schema["title"]
        if "type" in reduced_schema:
            del reduced_schema["type"]
        for k, v in reduced_schema["properties"].items():
            if "title" in v:
                del v["title"]

        # Ensure json with double quotes.
        schema_str = json.dumps(reduced_schema)

        return OUTPUT_FORMAT.format(schema=schema_str)

    def formatting_result(self, llm_output: str) -> T:
        """Parse llm_output and instantiate the result as provided pydantic_obj."""
        try:
            match = re.search(
                r"\{.*\}", llm_output.strip(), re.MULTILINE | re.IGNORECASE | re.DOTALL
            )
            json_str = match.group() if match else ""
            json_object = json.loads(json_str, strict=False)
            return self.pydantic_obj.parse_obj(json_object)
        except Exception as e:
            name = self.pydantic_obj.__name__
            msg = f"Failed to parse {name} from completion {llm_output}. Got: {e}"
            raise OutputParserError(msg, llm_output)
