import re
import time
from typing import Dict, List, Union

from broadcast_service import broadcast_service

from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.tools.arxiv.api_wrapper import ArxivAPIWrapper
from promptulate.tools.base import Tool
from promptulate.utils.core_utils import listdict_to_string, record_time


class ArxivQueryTool(Tool):
    name: str = "arxiv-query"
    description: str = (
        "A query tool around Arxiv.org "
        "Useful for when you need to answer questions about Physics, Mathematics, "
        "Computer Science, Quantitative Biology, Quantitative Finance, Statistics, "
        "Electrical Engineering, and Economics "
        "from scientific articles on arxiv.org. "
        "Input should be a search query."
    )
    api_wrapper: ArxivAPIWrapper = ArxivAPIWrapper()

    def _run(self, query: str, **kwargs) -> Union[str, List[Dict]]:
        """Arxiv query tool

        Args:
            query: the paper keyword or arxiv id
            **kwargs:
                return_type(Optional(str)):  return string default. If you want to
                return List[Dict] type data, you can set 'return_type'='original'.
                Moreover, you can pass the arguments of ArxivAPIWrapper

        Returns:
            String type default or List[Dict] arxiv query result.
        """
        kwargs.update({"from_callback": self.name})
        if re.match(r"\d{4}\.\d{5}(v\d+)?", query):
            result = self.api_wrapper.query(id_list=[query], **kwargs)
        else:
            result = self.api_wrapper.query(query, **kwargs)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result)


def _init_arxiv_reference_tool_llm():
    preset = "You are an Arxiv assistant whose task is to assist users in providing advice on academic papers. Your output can only follow the user's instructions, otherwise you will be punished."  # noqa: E501
    return ChatOpenAI(default_system_prompt=preset, temperature=0)


class ArxivReferenceTool(Tool):
    name: str = "arxiv-reference"
    description: str = (
        "Use this tool to find search related to the field."
        "Your input is a arxiv keyword query."
    )
    max_reference_num = 3
    reference_string: str = ""
    reference_counter: int = 0

    def __init__(self, llm: BaseLLM = None, **kwargs):
        self.llm: BaseLLM = llm or _init_arxiv_reference_tool_llm()
        super().__init__(**kwargs)

    @record_time()
    def _run(self, query: str, *args, **kwargs) -> Union[str, List[Dict]]:
        """
        Input arxiv paper information and return paper references.
        Args:
            query(str): arxiv paper information
            *args: Nothing
            **kwargs:
                return_type(Optional[str]): return string default. If you want to return
                List[Dict] type data, you can set 'return_type'='original.'
        Returns:
            String type or List[Dict] reference information
        """

        @broadcast_service.on_listen("ArxivReferenceTool.get_relevant_paper_info")
        @record_time()
        def get_relevant_paper_info(keyword: str):
            """return paper related information from keyword"""
            arxiv_query_tool = ArxivQueryTool()
            specified_fields = ["entry_id", "title"]
            queryset = arxiv_query_tool.run(
                keyword, num_results=6, specified_fields=specified_fields
            )
            self.reference_string += queryset
            self.reference_counter += 1

        def analyze_query_string(query_string: str) -> List[str]:
            """Analyze `[query]: keyword1, keyword2, keyword3` type data to return
            keywords list."""
            assert "[query]" in query_string
            query_string = query_string.split(":")[1]
            return query_string.split(",")

        def analyze_reference_string(reference_string: str) -> List[Dict]:
            pattern = r"\[(\d+)\]\s+(.+?),\s+(http://.+?);"
            references = []
            for match in re.finditer(pattern, reference_string):
                references.append({"title": match.group(2), "url": match.group(3)})
            return references

        self.reference_counter = 0
        prompt = (
            f"现在你需要根据其研究的具体内容，列出至少{self.max_reference_num}篇参考文献，你可以使用arxiv进行查询，你需要给我提供3个arxiv查询关键词，我将使用"
            f"arxiv进行查询，你需要根据我返回的结果选取最符合当前研究的{self.max_reference_num}篇参考文献。"
            f"用户输入:{query}"
            "你的输出必须是三个查询词\n，如 [query]: keyword1, keyword2, keyword3\n"
        )
        keywords = analyze_query_string(self.llm(prompt))
        for keyword in keywords:
            broadcast_service.broadcast(
                "ArxivReferenceTool.get_relevant_paper_info", keyword
            )

        while self.reference_counter < 3:
            time.sleep(0.2)

        prompt = (
            "Now you need to return the most appropriate 5 references \
            based on the papers given below\n"
            f"```{self.reference_string}```\n"
            "Your output format must be as follows:\nReferences:\n[1] [title1](url1);\n[2] [title2](url2);\n[3] [title3](url3);\n"  # noqa
        )
        # TODO If there is a problem with the returned format and an error is reported
        # then ask LLM to format the data
        result = self.llm(prompt)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return analyze_reference_string(result)
        return result


def _init_arxiv_summary_tool_llm():
    preset = """You are an Arxiv assistant whose task is to assist users in providing advice and assistance on academic papers. Your output can only follow the user's instructions, otherwise you will be punished."""  # Noqa
    return ChatOpenAI(default_system_prompt=preset, temperature=0)


class ArxivSummaryTool(Tool):
    name: str = "arxiv-summary"
    description: str = (
        "A summary tool that can be used to obtain a paper summary, listing "
        "key insights and lessons learned in the paper, and references in the paper"
        "Your input is a arxiv keyword query."
    )
    summary_string: str = ""
    summary_counter: int = 0

    def __init__(self, llm: BaseLLM = None, **kwargs):
        self.llm: BaseLLM = llm or _init_arxiv_summary_tool_llm()
        self.api_wrapper: ArxivAPIWrapper = ArxivAPIWrapper()
        super().__init__(**kwargs)

    def _run(self, query: str, **kwargs) -> str:
        """An arxiv paper summary tool that passes in the article name (or arxiv id) and
        returns summary results.

        Args:
            query: the keyword you want to query
            **kwargs:
                You can pass the arguments of ArxivAPIWrapper

        Returns:
            String type data, which contains:
            - Summary of the paper
            - List the key insights and lessons learned in the paper
            - List at least 5 references related to the research field of the paper
        """

        @broadcast_service.on_listen("ArxivSummaryTool.run.get_opinion")
        def get_opinion():
            prompt = (
                f"Based on the abstract of the paper below, please list the key insights from the paper and the lessons learned derived from it. Your output should be provided in bullet points ```{paper_summary}```"  # noqa
                "Please use the following output format:\nKey insights:\n{Key insights in bullet points}\nLessons learned:\n{Lessons learned in bullet points},with each point separated by a hyphen `-`"  # noqa
            )
            opinion = self.llm(prompt)
            self.summary_string += opinion + "\n"
            self.summary_counter += 1

        @broadcast_service.on_listen("ArxivSummaryTool.run.get_references")
        def get_references():
            arxiv_referencer_tool = ArxivReferenceTool()
            references = arxiv_referencer_tool.run(paper_summary)
            self.summary_string += references + "\n\n"
            self.summary_counter += 1

        @broadcast_service.on_listen("ArxivSummaryTool.run.get_advice")
        def get_advice():
            prompt = (
                f"Based on the abstract of the paper below, please provide 3-5 suggestions related to its topics or potential future research directions. Your output should be provided in bullet points  ```{paper_summary}```"  # noqa
                "Please use the following output format:\nRelated suggestions:\n{related suggestions in bullet points}, with each point separated by a hyphen `-`"  # noqa
            )
            opinion = self.llm(prompt)
            self.summary_string += opinion + "\n"
            self.summary_counter += 1

        self.summary_counter = 0
        if re.match(r"\d{4}\.\d{5}(v\d+)?", query):
            paper_info = self.api_wrapper.query(
                id_list=[query], num_results=1, specified_fields=["title", "summary"]
            )
        else:
            paper_info = self.api_wrapper.query(
                query, num_results=1, specified_fields=["title", "summary"]
            )
            if len(paper_info) == 0:
                return "Could not find relevant arxiv article."
        paper_summary = listdict_to_string(paper_info, item_suffix="\n")
        self.summary_string = paper_summary

        broadcast_service.publish("ArxivSummaryTool.run.get_references")
        time.sleep(0.01)
        broadcast_service.publish("ArxivSummaryTool.run.get_opinion")
        time.sleep(0.01)
        broadcast_service.publish("ArxivSummaryTool.run.get_advice")

        while self.summary_counter < 3:
            time.sleep(0.1)

        return self.summary_string
