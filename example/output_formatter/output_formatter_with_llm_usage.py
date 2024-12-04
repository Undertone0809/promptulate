"""This example show how to use JSONFormatter by ChatOpenAI."""

from typing import List

from pydantic import BaseModel, Field

from promptulate.llms import ChatOpenAI
from promptulate.output_formatter import OutputFormatter


class LLMResponse(BaseModel):
    provinces: List[str] = Field(description="List of provinces name")


def main():
    llm = ChatOpenAI()
    formatter = OutputFormatter(LLMResponse)

    prompt = (
        f"Please tell me the names of provinces in China.\n"
        f"{formatter.get_formatted_instructions()}"
    )
    llm_output = llm(prompt)
    response: LLMResponse = formatter.formatting_result(llm_output)
    print(response)


if __name__ == "__main__":
    main()
