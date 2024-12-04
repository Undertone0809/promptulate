from typing import Optional

import pytest
from pydantic import BaseModel, Field

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

func1_schema_of_define_tool = {
    "name": "mock tool",
    "description": "mock tool description",
    "properties": {},
    "type": "object",
}

func2_schema_of_define_tool = {
    "name": "mock tool",
    "description": "mock tool description",
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
    # test func 0
    tool = define_tool(
        name="mock tool",
        description="mock tool description",
        callback=func_0,
    )

    assert tool.name == "mock tool"
    assert tool.description == "mock tool description"

    resp: str = tool.run()
    assert resp == "result"

    assert tool.to_schema() == func1_schema_of_define_tool

    # test func 1
    tool = define_tool(
        name="mock tool",
        description="mock tool description",
        callback=func_1,
    )

    assert tool.name == "mock tool"
    assert tool.description == "mock tool description"

    resp: str = tool.run(a="a", b=1)
    assert resp == "result"

    assert tool.to_schema() == func2_schema_of_define_tool


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


def test_tool_cls_lack_of_parameters():
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
    """Test class' tool to convert to schema."""

    # define parameters by BaseModel
    class ToolParameters(BaseModel):
        param1: str = Field(description="param1 description")
        param2: Optional[str] = Field(description="param2 description")

    class MockTool(Tool):
        name = "mock tool"
        description = "mock tool description"
        parameters: BaseModel = ToolParameters

        def _run(self, param1: str, param2: Optional[str] = None):
            return "mock tool"

    tool = MockTool()
    result: str = tool.run(param1="param1", param2="param2")
    assert result == "mock tool"

    assert tool.to_schema() == {
        "name": "mock tool",
        "description": "mock tool description",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"description": "param1 description", "type": "string"},
                "param2": {"description": "param2 description", "type": "string"},
            },
            "required": ["param1"],
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
    name: str = "fake tool"
    description: str = "fake tool description"

    def _run(self, *args, **kwargs):
        return "fake tool result"


def test_base_tool_with_no_params_to_tool():
    """Test BaseTool convert to Tool"""
    tool: BaseTool = FakerBaseToolWithNOParams()
    new_tool: Tool = ToolImpl.from_base_tool(tool)

    assert new_tool.to_schema() == {
        "name": "fake tool",
        "description": "fake tool description",
    }


def test_args_to_kwargs_with_pydantic_model():
    class SampleParams(BaseModel):
        arg1: str = Field(description="This is arg1")
        arg2: int = Field(description="This is arg2")

    class SampleTool(Tool):
        name = "sample_tool"
        description = "A sample tool for testing"
        parameters = SampleParams

        def _run(self, *args, **kwargs):
            pass

    tool = SampleTool()
    result = tool._args_to_kwargs("value1", 2, extra="extra_value")
    assert result == {"arg1": "value1", "arg2": 2, "extra": "extra_value"}


def test_args_to_kwargs_with_dict_parameters():
    class DictParamTool(Tool):
        name = "dict_param_tool"
        description = "A tool with dict parameters"
        parameters = {
            "type": "object",
            "properties": {"param1": {"type": "string"}, "param2": {"type": "integer"}},
        }

        def _run(self, *args, **kwargs):
            pass

    tool = DictParamTool()
    result = tool._args_to_kwargs("value1", 2, extra="extra_value")
    assert result == {"param1": "value1", "param2": 2, "extra": "extra_value"}


def test_args_to_kwargs_with_no_parameters():
    class NoParamTool(Tool):
        name = "no_param_tool"
        description = "A tool with no parameters"

        def _run(self, *args, **kwargs):
            pass

    tool = NoParamTool()
    result = tool._args_to_kwargs("value1", 2, extra="extra_value")
    assert result == {"extra": "extra_value"}


def test_args_to_kwargs_with_kwargs_only():
    class SampleParams(BaseModel):
        arg1: str = Field(description="This is arg1")
        arg2: int = Field(description="This is arg2")

    class SampleTool(Tool):
        name = "sample_tool"
        description = "A sample tool for testing"
        parameters = SampleParams

        def _run(self, *args, **kwargs):
            pass

    tool = SampleTool()
    result = tool._args_to_kwargs(arg1="value1", arg2=2, extra="extra_value")
    assert result == {"arg1": "value1", "arg2": 2, "extra": "extra_value"}


def test_args_to_kwargs_with_mixed_args_and_kwargs():
    class SampleParams(BaseModel):
        arg1: str = Field(description="This is arg1")
        arg2: int = Field(description="This is arg2")

    class SampleTool(Tool):
        name = "sample_tool"
        description = "A sample tool for testing"
        parameters = SampleParams

        def _run(self, *args, **kwargs):
            pass

    tool = SampleTool()
    result = tool._args_to_kwargs("value1", arg2=2, extra="extra_value")
    assert result == {"arg1": "value1", "arg2": 2, "extra": "extra_value"}
