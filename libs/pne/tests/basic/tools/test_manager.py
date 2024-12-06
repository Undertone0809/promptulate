from typing import Callable, Dict

import pytest

from pne.tools.base import Tool, ToolKit
from pne.tools.manager import ToolManager


# Define a dummy function to be converted into a Tool
def dummy_function(param1: str, param2: int) -> str:
    """
    A dummy function that returns a formatted string.

    Args:
        param1: A string parameter.
        param2: An integer parameter.
    Returns:
        A string that combines param1 and param2.
    """
    return f"param1={param1}, param2={param2}"


# Another dummy function
def another_function(param: str) -> str:
    """
    Another dummy function for testing.

    Args:
        param: A string parameter.
    Returns:
        A reversed string.
    """
    return param[::-1]


# A dummy toolkit containing one tool
class MyToolKit(ToolKit):
    def __init__(self):
        super().__init__()

        @self.register
        def toolkit_function(x: str) -> str:
            """
            A function inside a toolkit.

            Args:
                x: A string parameter.

            Returns:
                String stating the parameter was processed.
            """
            return f"Processed {x}"


@pytest.fixture
def tool_manager():
    # Create tools from the functions
    t1 = Tool.from_function(dummy_function)
    t2 = Tool.from_function(another_function)
    toolkit = MyToolKit()
    # Initialize the ToolManager with multiple types of tools
    manager = ToolManager([t1, t2, toolkit])
    return manager


def test_get_tool(tool_manager):
    tool = tool_manager.get_tool("dummy_function")
    assert tool is not None
    assert tool.name == "dummy_function"

    non_existent_tool = tool_manager.get_tool("non_existent")
    assert non_existent_tool is None


def test_run_tool_with_dict_parameters(tool_manager):
    # Run the dummy_function with dict parameters
    output = tool_manager.run_tool("dummy_function", {"param1": "hello", "param2": 42})
    assert output == "param1=hello, param2=42"


def test_run_tool_with_string_parameters(tool_manager):
    # Run the another_function with string parameters
    output = tool_manager.run_tool("another_function", "hello")
    assert output == "olleh"


def test_run_unknown_tool(tool_manager):
    # Attempt to run a non-existent tool
    output = tool_manager.run_tool("unknown_tool", {})
    assert "has not been provided yet" in output


def test_run_tool_from_toolkit(tool_manager):
    output = tool_manager.run_tool("toolkit_function", {"x": "myvalue"})
    assert output == "Processed myvalue"


def test_tool_names(tool_manager):
    names = tool_manager.tool_names
    # Should contain the names of dummy_function, another_function, and toolkit_function
    assert "dummy_function" in names
    assert "another_function" in names
    assert "toolkit_function" in names


def test_tool_descriptions(tool_manager):
    descriptions = tool_manager.tool_descriptions
    # The descriptions should be JSON representations of the tool functions
    assert "dummy_function" in descriptions
    assert "another_function" in descriptions
    assert "toolkit_function" in descriptions


def test_tool_call_schemas(tool_manager):
    schemas = tool_manager.tool_call_schemas
    assert len(schemas) == 3
    # Check that each schema is a dict with the expected keys
    for schema in schemas:
        assert "function" in schema
        assert "type" in schema
        assert schema["type"] == "function"
        func_info = schema["function"]
        assert "name" in func_info
        assert "description" in func_info
        assert "parameters" in func_info


def test_function_call_schemas(tool_manager):
    schemas = tool_manager.function_call_schemas
    assert len(schemas) == 3
    for schema in schemas:
        assert "name" in schema
        assert "description" in schema
        assert "parameters" in schema
        assert "properties" in schema["parameters"]
        assert "required" in schema["parameters"]


class TestToolKit(ToolKit):
    """A test toolkit for testing purposes."""

    def __init__(self):
        super().__init__()

        # Register tools in the constructor
        @self.register
        def tool2(a: float) -> float:
            """Square a number.

            Args:
                a: Number to square

            Returns:
                Square of the input
            """
            return a * a

        @self.register
        def tool3(text: str) -> str:
            """Convert text to uppercase.

            Args:
                text: Text to convert

            Returns:
                Uppercase text
            """
            return text.upper()


def test_add_tool():
    # Initialize empty manager
    manager = ToolManager([])
    assert len(manager.tools) == 0

    # Add a single tool
    def tool1(x: int, y: int) -> int:
        """Add two numbers.

        Args:
            x: First number
            y: Second number

        Returns:
            Sum of x and y
        """
        return x + y

    t1 = Tool.from_function(tool1)
    manager.add_tool(t1)
    assert len(manager.tools) == 1
    assert "tool1" in manager.tools
    assert manager.tools["tool1"] == t1

    # Add a function tool directly
    def test_func(name: str) -> str:
        """Return a greeting.

        Args:
            name: Name to greet

        Returns:
            Greeting message
        """
        return f"Hello {name}"

    manager.add_tool(test_func)
    assert len(manager.tools) == 2
    assert "test_func" in manager.tools
    assert isinstance(manager.tools["test_func"], Tool)

    # Add a toolkit
    toolkit = TestToolKit()  # Create an instance of our test toolkit
    manager.add_tool(toolkit)
    assert len(manager.tools) == 4
    assert "tool2" in manager.tools
    assert "tool3" in manager.tools
    assert isinstance(manager.tools["tool2"], Tool)
    assert isinstance(manager.tools["tool3"], Tool)

    # Test adding invalid tool type
    with pytest.raises(ValueError, match="Unknown tool type"):
        manager.add_tool(123)
