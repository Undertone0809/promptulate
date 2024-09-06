from promptulate.tools.shell import ShellTool


def test_shell_tool():
    tool = ShellTool()
    command = """echo hello"""
    result = tool.run(command)
    assert result in ["hello", "hello\r\n"]
