from promptulate.tools.python_repl.tools import PythonREPLTool
from promptulate.utils.logger import logger


def test_tool():
    tool = PythonREPLTool()
    command = """print(16.5 ** 0.43)"""
    result = tool.run(command)
    logger.info(result)
