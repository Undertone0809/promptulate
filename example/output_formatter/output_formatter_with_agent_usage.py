"""This example show how to use JSONFormatter by Agent."""
from promptulate.agents import WebAgent
from promptulate.pydantic_v1 import BaseModel, Field


class Response(BaseModel):
    city: str = Field(description="City name")
    temperature: float = Field(description="Temperature in Celsius")


def main():
    agent = WebAgent()
    prompt = "What is the temperature in Shanghai tomorrow?"
    response: Response = agent.run(prompt=prompt, output_schema=Response)
    print(response.city, response.temperature)


if __name__ == "__main__":
    main()
