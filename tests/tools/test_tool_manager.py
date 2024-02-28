def test_get_tool():
    tool_1 = Tool1()
    tool_2 = Tool2()
    tool_manager = ToolManager(tools=[tool_1, tool_2, tool_3])
    tool = tool_manager.get_tool("Tool1")
    assert tool.to_schema() == tool_1.to_schema()

    tool = tool_manager.get_tool("Tool2")
    assert tool.to_schema() == {
        "name": "Tool2",
        "description": "This is tool2",
    }

    tool = tool_manager.get_tool("tool_3")
    assert tool.to_schema() == {
        "type": "object",
        "properties": {"age": {"type": "string"}},
        "required": ["age"],
        "description": "This is tool3",
        "name": "tool_3",
    }

    tool = tool_manager.get_tool("no exist")
    assert tool is None
    tool_1 = Tool1()
    tool_2 = Tool2()
    tool_manager = ToolManager(tools=[tool_1, tool_2, tool_3])
    tool = tool_manager.get_tool("Tool1")
    assert tool.to_schema() == tool_1.to_schema()

    tool = tool_manager.get_tool("Tool2")
    assert tool.to_schema() == {
        "name": "Tool2",
        "description": "This is tool2",
    }

    tool = tool_manager.get_tool("tool_3")
    assert tool.to_schema() == {
        "type": "object",
        "properties": {"age": {"type": "string"}},
        "required": ["age"],
        "description": "This is tool3",
        "name": "tool_3",
    }

    tool = tool_manager.get_tool("no exist")
    assert tool is None


def test_run_tool():
    tool_manager = ToolManager(tools=[tool_3])
    result: str = tool_manager.run_tool("tool_3", {"age": "20"})
    assert result == "tool 3 result"


def test_tool_names():
    tool_1 = Tool1()
    tool_2 = Tool2()
    tool_manager = ToolManager(tools=[tool_1, tool_2, tool_3])
    assert tool_manager.tool_names == "Tool1, Tool2, tool_3"


def test_tool_descriptions():
    tool_1 = Tool1()
    tool_2 = Tool2()
    tool_manager = ToolManager(tools=[tool_1, tool_2, tool_3])
    assert (
        tool_manager.tool_descriptions
        == '{"name": "Tool1", "description": "This is tool1"}\n{"name": "Tool2", "description": "This is tool2"}\n{"type": "object", "properties": {"age": {"type": "string"}}, "required": ["age"], "description": "This is tool3", "name": "tool_3"}\n'  # noqa
    )
