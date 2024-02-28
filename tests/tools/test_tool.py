from typing import Optional

import pytest

from promptulate.pydantic_v1 import BaseModel, Field
from promptulate.tools.base import (
    BaseTool,
    Tool,
    ToolImpl,
    define_tool,
    function_to_tool,
    function_to_tool_schema,
)


def func_0():
    """mock func 0"""
    return "result"


func_0_schema = {
    "description": "mock func 0",
    "name": "func_0",
    "properties": {},
    "type": "object",
}


def func_1(a: str, b: int):
    """mock func 1"""
    return "result"


func_1_schema = {
    "type": "object",
    "properties": {
        "a": {
            "type": "string",
        },
        "b": {
            "type": "integer",
        },
    },
    "required": ["a", "b"],
    "description": "mock func 1",
    "name": "func_1",
}


def func_2(a: str, b: Optional[int] = None):
    """mock func 2"""
    return "result"


func_2_schema = {
    "description": "mock func 2",
    "name": "func_2",
    "properties": {
        "a": {
            "type": "string",
        },
        "b": {
            "type": "integer",
        },
    },
    "required": ["a"],
    "type": "object",
}


def func_3(a: str, b: int = 10):
    """mock func 3"""
    return "result"


func_3_schema = {
    "description": "mock func 3",
    "name": "func_3",
    "properties": {
        "a": {
            "type": "string",
        },
        "b": {
            "default": 10,
            "type": "integer",
        },
    },
    "required": ["a"],
    "type": "object",
}


def func_4(a: str, b: int):
    """mock tool description"""
    return "result"


func_4_schema = {
    "description": "mock tool description",
    "name": "func_4",
    "properties": {
        "a": {
            "type": "string",
        },
        "b": {
            "type": "integer",
        },
    },
    "required": ["a", "b"],
    "type": "object",
}


def test_define_tool():
    """Test initialize tool by define_tool function."""
    tool = define_tool(
        name="mock tool",
        description="mock tool description",
        callback=func_0,
    )

    assert tool.name == "mock tool"
    assert tool.description == "mock tool description\nmock func 0"

    resp: str = tool.run()
    assert resp == "result"

    assert tool.to_schema() == func_0_schema


def test_tool_cls():
    """Test initialize tool by Tool class."""

    # test basic custom Tool
    class MockTool(Tool):
        name = "mock tool"
        description = "mock tool description"

        def _run(self):
            return "mock tool"

    tool = MockTool()
    assert tool.name == "mock tool"
    assert tool.description == "mock tool description"

    resp: str = tool.run()
    assert resp == "mock tool"

    print(tool.to_schema())

    # test custom Tool but lack of name
    class ToolWithLackParam(Tool):
        name = "mock tool"

        def _run(self):
            return "mock tool"

    with pytest.raises(TypeError):
        ToolWithLackParam()

    # test custom Tool but lack of description
    class ToolWithLackParam(Tool):
        description = "mock tool"

        def _run(self):
            return "mock tool"

    with pytest.raises(TypeError):
        ToolWithLackParam()


def test_tool_class_parameter():
    """Test class' tool to covert to schema."""

    # define parameters by BaseModel
    class Parameters(BaseModel):
        param1: Optional[str] = Field(description="param1 description")
        param2: str = Field(description="param2 description")

    class MockTool(Tool):
        name = "mock tool"
        description = "mock tool description"
        parameters = Parameters

        def _run(self):
            return "mock tool"

    tool = MockTool()

    assert tool.to_schema() == {
        "name": "mock tool",
        "description": "mock tool description",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"description": "param1 description", "type": "string"},
                "param2": {"description": "param2 description", "type": "string"},
            },
            "required": ["param2"],
        },
    }


def test_function_to_tool_schema():
    tool_schema: dict = function_to_tool_schema(func_1)
    assert tool_schema == func_1_schema

    tool_schema: dict = function_to_tool_schema(func_2)
    assert tool_schema == func_2_schema

    tool_schema: dict = function_to_tool_schema(func_3)
    assert tool_schema == func_3_schema

    tool_schema: dict = function_to_tool_schema(func_4)
    assert tool_schema == func_4_schema

    tool_schema: dict = function_to_tool_schema(func_0)
    assert tool_schema == func_0_schema


def test_function_to_tool():
    tool: Tool = function_to_tool(func_1)
    assert tool.to_schema() == func_1_schema

    tool: Tool = function_to_tool(func_2)
    assert tool.to_schema() == func_2_schema

    tool: Tool = function_to_tool(func_3)
    assert tool.to_schema() == func_3_schema

    tool: Tool = function_to_tool(func_4)
    assert tool.to_schema() == func_4_schema

    tool: Tool = function_to_tool(func_0)
    assert tool.to_schema() == func_0_schema


class FakerBaseToolParams(BaseModel):
    arg1: str = Field(..., description="This is arg1")
    arg2: Optional[int] = Field(default=1, description="This is arg2")


class FakerBaseToolWithParams(BaseTool):
    name: str = Field(default="fake tool")
    description: str = Field(default="fake tool description")
    parameters: BaseModel = Field(default=FakerBaseToolParams)

    def _run(self, *args, **kwargs):
        return "fake tool result"


def test_base_tool_with_params_to_tool():
    """Test the conversion of BaseTool to Tool when the tool has parameters."""
    """Test BaseTool convert to Tool"""
    tool: BaseTool = FakerBaseToolWithParams()
    new_tool: Tool = ToolImpl.from_base_tool(tool)

    assert new_tool.to_schema() == {
        "name": "fake tool",
        "description": "fake tool description",
        "parameters": {
            "type": "object",
            "properties": {
                "arg1": {"description": "This is arg1", "type": "string"},
                "arg2": {
                    "default": 1,
                    "description": "This is arg2",
                    "type": "integer",
                },
            },
            "required": ["arg1"],
        },
    }


class FakerBaseToolWithNOParams(BaseTool):
    name = "fake tool"
    description = "fake tool description"

    def _run(self, *args, **kwargs):
        return "fake tool result"


def test_base_tool_with_no_params_to_tool():
    """Test the conversion of BaseTool to Tool when the tool has no parameters."""
    """Test BaseTool convert to Tool"""
    tool: BaseTool = FakerBaseToolWithNOParams()
    new_tool: Tool = ToolImpl.from_base_tool(tool)

    assert new_tool.to_schema() == {
        "name": "fake tool",
        "description": "fake tool description",
    }
