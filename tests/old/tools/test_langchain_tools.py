import os
from tempfile import TemporaryDirectory

from langchain.agents.agent_toolkits import FileManagementToolkit

from promptulate.tools.langchain.tools import LangchainTool


def test_read_file():
    working_directory = TemporaryDirectory()

    lc_write_tool = FileManagementToolkit(
        root_dir=str(working_directory.name),
        selected_tools=["write_file"],
    ).get_tools()[0]

    tool = LangchainTool(lc_write_tool)
    tool.run({"file_path": "example.txt", "text": "Hello World!"})

    assert os.path.exists(os.path.join(working_directory.name, "example.txt"))
