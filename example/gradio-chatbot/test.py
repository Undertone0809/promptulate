import promptulate as pne
from promptulate.tools.duckduckgo.tools import DuckDuckGoTool


def web_search(keyword: str) -> str:
    """search by keyword in web.
    Args:
        keyword: keyword to search

    Returns:
        str: search result
    """
    return DuckDuckGoTool().run(keyword)


agent = pne.ToolAgent(tools=[web_search])
resp: str = agent.run("How will the temperature be in New York tomorrow?")
