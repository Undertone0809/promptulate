import os
import tempfile

import pytest

from promptulate.tools.file.toolkit import FileToolKit
from promptulate.tools.file.tools import (
    AppendFileTool,
    CopyFileTool,
    DeleteFileTool,
    ListDirectoryTool,
    MoveFileTool,
    ReadFileTool,
    WriteFileTool,
)


class TestFileToolKit:
    # create a temporary directory
    temp_dir = tempfile.TemporaryDirectory().name

    def test_validate_root_dir(self):
        # Test when root_dir is None,
        # root_dir will be assigned to the current working directory
        toolkit = FileToolKit(root_dir=None)
        assert toolkit.root_dir == os.getcwd()

        # Test when root_dir is an empty string,
        # root_dir will be assigned to the current working directory
        toolkit1 = FileToolKit(root_dir="")
        assert toolkit1.root_dir == os.getcwd()

        # Test when root_dir is a valid directory,
        # root_dir will be assigned to the given directory
        toolkit2 = FileToolKit(root_dir=self.temp_dir)
        assert toolkit2.root_dir == self.temp_dir

    # tools name is a list of all the tools in the toolkit
    tools_name = [
        "write-file",
        "append-file",
        "read-file",
        "delete-file",
        "list-directory",
        "copy-file",
        "move-file",
    ]

    def test_validate_tools(self):
        # Test when mode_List is None,
        # tools will be assigned to all tools
        toolkit = FileToolKit(root_dir=self.temp_dir, modes=None)
        tools = toolkit.get_tools()
        assert len(tools) == 7
        for tool, Tname in zip(tools, self.tools_name):
            assert tool.name == Tname

        # Test when mode_List is an empty list,
        # tools will be assigned to all tools
        toolkit1 = FileToolKit(root_dir=self.temp_dir, modes=[])
        tools = toolkit1.get_tools()
        assert len(tools) == 7
        for tool, Tname in zip(tools, self.tools_name):
            assert tool.name == Tname

        # Tests that mode_List does not throw an exception
        # when it contains an existing tool
        toolkit2 = FileToolKit(root_dir=self.temp_dir, modes=["write", "read"])
        tools = toolkit2.get_tools()
        assert len(tools) == 2
        assert tools[0].name == "write-file"
        assert tools[1].name == "read-file"

        # Test raises ValueError
        # when mode_List contains a tool that does not exist
        with pytest.raises(ValueError):
            FileToolKit(root_dir=self.temp_dir, modes=["write", "nonexistent"])


class TestFileTools:
    # Create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    dir_name = temp_dir.name
    # Create a second temporary directory
    temp_dir2 = tempfile.TemporaryDirectory()
    dir_name2 = temp_dir2.name

    # Create a file
    temp_file = "test.txt"

    def test_list_directory_tool(self):
        # Test ListDirectoryTool's run method
        list_tool = ListDirectoryTool(self.dir_name)
        assert list_tool.run() == ""
        assert list_tool.to_schema()["name"] == "list-directory"

    def test_write_file_tool(self):
        # Test WriteFileTool's run method
        write_tool = WriteFileTool(self.dir_name)
        write_tool.run(self.temp_file, "test")
        assert open(self.dir_name + "/" + self.temp_file).read() == "test"
        assert write_tool.to_schema()["parameters"] == {
            "properties": {
                "file_name": {
                    "description": "The name of the file you want to edit.",
                    "type": "string",
                },
                "text": {
                    "description": "The content you want to edit.",
                    "type": "string",
                },
            },
            "required": ["file_name"],
            "type": "object",
        }

    def test_read_file_tool(self):
        # Test ReadFileTool's run method
        read_tool = ReadFileTool(self.dir_name)
        assert (
            read_tool.run(self.temp_file)
            == open(self.dir_name + "/" + self.temp_file).read()
        )
        assert read_tool.to_schema()["parameters"] == {
            "properties": {
                "file_name": {
                    "description": "The name of the file you want to edit.",
                    "type": "string",
                }
            },
            "required": ["file_name"],
            "type": "object",
        }

    def test_append_file_tool(self):
        # Test AppendFileTool's run method
        append_tool = AppendFileTool(self.dir_name)
        append_tool.run(self.temp_file, "test")
        assert open(self.dir_name + "/" + self.temp_file).read() == "testtest"
        assert append_tool.to_schema()["parameters"] == {
            "properties": {
                "file_name": {
                    "description": "The name of the file you want to edit.",
                    "type": "string",
                },
                "text": {
                    "description": "The content you want to edit.",
                    "type": "string",
                },
            },
            "required": ["file_name"],
            "type": "object",
        }

    def test_delete_file_tool(self):
        # Test DeleteFileTool's run method
        delete_tool = DeleteFileTool(self.dir_name)
        delete_tool.run(self.temp_file)
        assert not os.path.exists(self.dir_name + "/" + self.temp_file)
        assert delete_tool.to_schema()["parameters"] == {
            "properties": {
                "file_name": {
                    "description": "The name of the file you want to edit.",
                    "type": "string",
                }
            },
            "required": ["file_name"],
            "type": "object",
        }

    def test_copy_file_tool(self):
        # Test CopyFileTool's run method
        with open(f"{self.dir_name}/{self.temp_file}", "w") as file:
            file.write("test")
        copy_tool = CopyFileTool(self.dir_name)
        copy_tool.run(self.temp_file, self.dir_name2)
        assert os.path.exists(f"{self.dir_name2}/{self.temp_file}")
        assert copy_tool.to_schema()["parameters"] == {
            "properties": {
                "file_name": {
                    "description": "The name of the file you want to edit.",
                    "type": "string",
                },
                "destination_path": {
                    "description": "The directory you want to reach.",
                    "type": "string",
                },
            },
            "required": ["file_name", "destination_path"],
            "type": "object",
        }

    def test_move_file_tool(self):
        # Test MoveFileTool's run method
        with open(f"{self.dir_name}/{self.temp_file}", "w") as file:
            file.write("test")
        move_tool = MoveFileTool(self.dir_name)
        move_tool.run(self.temp_file, self.dir_name2)
        assert os.path.exists(f"{self.dir_name2}/{self.temp_file}")
        assert not os.path.exists(f"{self.dir_name}/{self.temp_file}")
        assert move_tool.to_schema()["parameters"] == {
            "properties": {
                "file_name": {
                    "description": "The name of the file you want to edit.",
                    "type": "string",
                },
                "destination_path": {
                    "description": "The directory you want to reach.",
                    "type": "string",
                },
            },
            "required": ["file_name", "destination_path"],
            "type": "object",
        }
