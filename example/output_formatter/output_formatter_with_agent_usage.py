"""This example show how to use JSONFormatter by Agent."""
from pydantic import BaseModel, Field

from promptulate.agents import WebAgent


class JSONResponse(BaseModel):
    city: str = Field(description="City name")
    temperature: float = Field(description="Temperature in Celsius")


def main():
    agent = WebAgent()
    prompt = f"What is the temperature in Shanghai tomorrow?"
    response: JSONResponse = agent.run(prompt=prompt, output_schema=JSONResponse)
    print(response)


if __name__ == "__main__":
    main()
