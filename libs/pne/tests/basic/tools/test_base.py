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
        function=lambda param1, param2: f"{param1} {param2}",
    )

    schema = tool.to_tool_schema()

    assert schema["type"] == "function"
    assert schema["function"]["name"] == "test_tool"
    assert schema["function"]["description"] == "A test tool"
    assert schema["function"]["parameters"]["type"] == "object"
    assert "param1" in schema["function"]["parameters"]["properties"]
    assert "param2" in schema["function"]["parameters"]["properties"]
    assert schema["function"]["parameters"]["required"] == ["param1"]


def test_class_method():
    """Test creating Tool from a class method."""

    class SampleClass:
        def sample_method(self, param1: str, param2: int = 10) -> str:
            """Sample class method for testing.

            Args:
                param1: First parameter
                param2: Second parameter with default value, but not required

            Returns:
                A string result
            """
            return f"{param1} {param2}"

    instance = SampleClass()
    tool = Tool.from_function(instance.sample_method)

    assert tool.name == "sample_method"
    assert "Sample class method for testing" in tool.description
    assert isinstance(tool.parameters, ToolParameters)
    assert "param1" in tool.parameters.properties
    assert "param2" in tool.parameters.properties
    assert tool.parameters.properties["param1"]["type"] == "string"
    assert tool.parameters.properties["param2"]["type"] == "integer"
    assert "param1" in tool.parameters.required
    assert "param2" not in tool.parameters.required


def test_tool_run():
    """Test running a tool with different function types."""

    # Test with simple function
    def sample_function(param1: str, param2: int = 10) -> str:
        """Sample function for testing."""
        return f"{param1} {param2}"

    tool = Tool.from_function(sample_function)
    result = tool.run(param1="hello", param2=20)
    assert result == "hello 20"

    # Test with default parameter
    result = tool.run(param1="world")
    assert result == "world 10"

    # Test with class method
    class SampleClass:
        def sample_method(self, param1: str, param2: int = 10) -> str:
            """Sample class method for testing."""
            return f"{param1}-{param2}"

    instance = SampleClass()
    tool = Tool.from_function(instance.sample_method)
    result = tool.run(param1="test", param2=30)
    assert result == "test-30"

    # Test with lambda function
    tool = Tool(
        name="lambda_tool",
        description="A tool with lambda function",
        parameters=ToolParameters(
            properties={
                "x": {"type": "integer"},
                "y": {"type": "integer"},
            },
            required=["x", "y"],
        ),
        function=lambda x, y: x + y,
    )
    result = tool.run(x=5, y=3)
    assert result == 8


def test_tool_run_with_args_kwargs():
    """Test running a tool with both positional and keyword arguments."""

    def func_with_args_kwargs(*args, **kwargs):
        """Test function that accepts both args and kwargs."""
        args_str = ", ".join(map(str, args))
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        return f"args: [{args_str}], kwargs: {{{kwargs_str}}}"

    tool = Tool(
        name="args_kwargs_tool",
        description="A tool that accepts both args and kwargs",
        parameters=ToolParameters(
            properties={
                "args": {"type": "array"},
                "kwargs": {"type": "object"},
            },
            required=[],
        ),
        function=func_with_args_kwargs,
    )

    # Test with only positional args
    result = tool.run(1, "test", True)
    assert result == "args: [1, test, True], kwargs: {}"

    # Test with only kwargs
    result = tool.run(x=1, y="hello")
    assert result == "args: [], kwargs: {x=1, y=hello}"

    # Test with both args and kwargs
    result = tool.run(42, name="test", flag=True)
    assert result == "args: [42], kwargs: {name=test, flag=True}"

    # Test with no arguments
    result = tool.run()
    assert result == "args: [], kwargs: {}"


def test_invalid_function():
    """Test creating Tool from function without docstring."""

    def invalid_function(param: str):
        return param

    with pytest.raises(ValueError):
        Tool.from_function(invalid_function)
