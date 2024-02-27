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
    # 创建临时目录
    temp_dir = tempfile.TemporaryDirectory().name

    def test_validate_root_dir(self):
        # 测试当root_dir为None时，root_dir会被赋值为当前工作目录
        toolkit = FileToolKit(root_dir=None)
        assert toolkit.root_dir == os.getcwd()

        # 测试当root_dir为空字符串时，root_dir会被赋值为当前工作目录
        toolkit1 = FileToolKit(root_dir="")
        assert toolkit1.root_dir == os.getcwd()

        # 测试当root_dir为有效路径时，root_dir会被赋值为该路径
        toolkit2 = FileToolKit(root_dir=self.temp_dir)
        assert toolkit2.root_dir == self.temp_dir

    def test_validate_tools(self):
        # 测试当selected_tools为None时，不会抛出异常
        toolkit = FileToolKit(root_dir=self.temp_dir, modes=None)
        assert toolkit.modes is None

        # 测试当selected_tools包含为None时，get_tools()返回所有工具
        toolkit2 = FileToolKit(root_dir=self.temp_dir, modes=[])
        tools = toolkit2.get_tools()
        assert len(tools) == 7

        # 测试当selected_tools为空列表时，不会抛出异常
        toolkit1 = FileToolKit(root_dir=self.temp_dir, modes=[])
        assert toolkit1.modes == []

        # 测试当selected_tools包含为空列表时，get_tools()返回所有工具
        toolkit2 = FileToolKit(root_dir=self.temp_dir, modes=[])
        tools = toolkit2.get_tools()
        assert len(tools) == 7

        # 测试当selected_tools包含存在的工具时，不会抛出异常
        toolkit2 = FileToolKit(root_dir=self.temp_dir, modes=["write", "read"])
        assert toolkit2.modes == ["write", "read"]

        # 测试当selected_tools包含存在的工具时，get_tools()返回对应的工具
        toolkit2 = FileToolKit(root_dir=self.temp_dir, modes=["write", "read"])
        tools = toolkit2.get_tools()
        assert len(tools) == 2

        # 测试当selected_tools包含不存在的工具时，会抛出ValueError
        with pytest.raises(ValueError):
            FileToolKit(root_dir=self.temp_dir, modes=["write", "nonexistent"])


class TestFileTools:
    # 创建临时目录
    temp_dir = tempfile.TemporaryDirectory()
    dir_name = temp_dir.name
    # 创建临时目录2
    temp_dir2 = tempfile.TemporaryDirectory()
    dir_name2 = temp_dir2.name

    # 创建临时文件
    temp_file = "test.txt"

    def test_list_directory_tool(self):
        # 测试ListDirectoryTool的run方法
        Ltools = ListDirectoryTool(self.dir_name)
        assert Ltools.run() == ""

    def test_write_file_tool(self):
        # 测试WriteFileTool的run方法
        Wtools = WriteFileTool(self.dir_name)
        Wtools.run(self.temp_file, "test")
        assert open(self.dir_name + "/" + self.temp_file).read() == "test"

    def test_read_file_tool(self):
        # 测试ReadFileTool的run方法
        Rtools = ReadFileTool(self.dir_name)
        assert (
            Rtools.run(self.temp_file)
            == open(self.dir_name + "/" + self.temp_file).read()
        )

    def test_append_file_tool(self):
        # 测试AppendFileTool的run方法
        Atools = AppendFileTool(self.dir_name)
        Atools.run(self.temp_file, "test")
        assert open(self.dir_name + "/" + self.temp_file).read() == "testtest"

    def test_delete_file_tool(self):
        # 测试DeleteFileTool的run方法
        Dtools = DeleteFileTool(self.dir_name)
        Dtools.run(self.temp_file)
        assert not os.path.exists(self.dir_name + "/" + self.temp_file)

    def test_copy_file_tool(self):
        # 测试CopyFileTool的run方法
        with open(f"{self.dir_name}/{self.temp_file}", "w") as file:
            file.write("test")
        Ctools = CopyFileTool(self.dir_name)
        Ctools.run(self.temp_file, self.dir_name2)
        assert os.path.exists(f"{self.dir_name2}/{self.temp_file}")

    def test_move_file_tool(self):
        # 测试MoveFileTool的run方法
        with open(f"{self.dir_name}/{self.temp_file}", "w") as file:
            file.write("test")
        Mtools = MoveFileTool(self.dir_name)
        Mtools.run(self.temp_file, self.dir_name2)
        assert os.path.exists(f"{self.dir_name2}/{self.temp_file}")
        assert not os.path.exists(f"{self.dir_name}/{self.temp_file}")
