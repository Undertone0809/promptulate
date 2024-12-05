import pytest

from pne.tools.base import Tool, ToolParameters


def test_function():
    """Test function for creating a Tool instance."""

    def sample_function(param1: str, param2: int = 10) -> str:
        """Sample function for testing.

        Args:
            param1: First parameter
            param2: Second parameter with default value, but not required

        Returns:
            A string result
        """
        return f"{param1} {param2}"

    tool = Tool.from_function(sample_function)

    assert tool.name == "sample_function"
    assert "Sample function for testing" in tool.description
    assert isinstance(tool.parameters, ToolParameters)
    assert "param1" in tool.parameters.properties
    assert "param2" in tool.parameters.properties
    assert tool.parameters.properties["param1"]["type"] == "string"
    assert tool.parameters.properties["param2"]["type"] == "integer"
    assert "param1" in tool.parameters.required
    assert "param2" not in tool.parameters.required


def test_to_tool_call_schema():
    """Test converting Tool to OpenAI function schema format."""
    tool = Tool(
        name="test_tool",
        description="A test tool",
        parameters=ToolParameters(
            properties={
                "param1": {"type": "string"},
                "param2": {"type": "integer"},
            },
            required=["param1"],
        ),
    )

    schema = tool.to_tool_call_schema()

    assert schema["type"] == "function"
    assert schema["function"]["name"] == "test_tool"
    assert schema["function"]["description"] == "A test tool"
    assert schema["function"]["parameters"]["type"] == "object"
    assert "param1" in schema["function"]["parameters"]["properties"]
    assert "param2" in schema["function"]["parameters"]["properties"]
    assert schema["function"]["parameters"]["required"] == ["param1"]


def test_invalid_function():
    """Test creating Tool from function without docstring."""

    def invalid_function(param: str):
        return param

    with pytest.raises(ValueError):
        Tool.from_function(invalid_function)
