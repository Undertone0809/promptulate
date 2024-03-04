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

    def test_validate_tools(self):
        # Test when mode_List is None,
        # tools will be assigned to all tools
        toolkit = FileToolKit(root_dir=self.temp_dir, modes=None)
        tools = toolkit.get_tools()
        assert len(tools) == 7

        # Test when mode_List is an empty list,
        # tools will be assigned to all tools
        toolkit1 = FileToolKit(root_dir=self.temp_dir, modes=[])
        tools = toolkit1.get_tools()
        assert len(tools) == 7

        # Tests that mode_List does not throw an exception
        # when it contains an existing tool
        toolkit2 = FileToolKit(root_dir=self.temp_dir, modes=["write", "read"])
        assert toolkit2.modes == ["write", "read"]

        # Tests that mode_List returns the corresponding tool
        # when it contains an existing tool
        toolkit3 = FileToolKit(root_dir=self.temp_dir, modes=["write", "read"])
        tools = toolkit3.get_tools()
        assert len(tools) == 2

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
        Ltools = ListDirectoryTool(self.dir_name)
        assert Ltools.run() == ""

    def test_write_file_tool(self):
        # Test WriteFileTool's run method
        Wtools = WriteFileTool(self.dir_name)
        Wtools.run(self.temp_file, "test")
        assert open(self.dir_name + "/" + self.temp_file).read() == "test"

    def test_read_file_tool(self):
        # Test ReadFileTool's run method
        Rtools = ReadFileTool(self.dir_name)
        assert (
            Rtools.run(self.temp_file)
            == open(self.dir_name + "/" + self.temp_file).read()
        )

    def test_append_file_tool(self):
        # Test AppendFileTool's run method
        Atools = AppendFileTool(self.dir_name)
        Atools.run(self.temp_file, "test")
        assert open(self.dir_name + "/" + self.temp_file).read() == "testtest"

    def test_delete_file_tool(self):
        # Test DeleteFileTool's run method
        Dtools = DeleteFileTool(self.dir_name)
        Dtools.run(self.temp_file)
        assert not os.path.exists(self.dir_name + "/" + self.temp_file)

    def test_copy_file_tool(self):
        # Test CopyFileTool's run method
        with open(f"{self.dir_name}/{self.temp_file}", "w") as file:
            file.write("test")
        Ctools = CopyFileTool(self.dir_name)
        Ctools.run(self.temp_file, self.dir_name2)
        assert os.path.exists(f"{self.dir_name2}/{self.temp_file}")

    def test_move_file_tool(self):
        # Test MoveFileTool's run method
        with open(f"{self.dir_name}/{self.temp_file}", "w") as file:
            file.write("test")
        Mtools = MoveFileTool(self.dir_name)
        Mtools.run(self.temp_file, self.dir_name2)
        assert os.path.exists(f"{self.dir_name2}/{self.temp_file}")
        assert not os.path.exists(f"{self.dir_name}/{self.temp_file}")
