import re
import time
from typing import List, Dict, Union

from broadcast_service import broadcast_service

from promptulate.llms.base import BaseLLM
from promptulate.llms.openai import ChatOpenAI
from promptulate.tools.arxiv.api_wrapper import ArxivAPIWrapper
from promptulate.tools.base import Tool
from promptulate.utils.core_utils import record_time, listdict_to_string
from promptulate.utils.logger import get_logger

logger = get_logger()


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
                return_type(Optional(str)):  return string default. If you want to return List[Dict] type data,
                you can set 'return_type'='original'
                Moreover, you can pass the arguments of ArxivAPIWrapper

        Returns:
            String type default or List[Dict] arxiv query result.
        """
        kwargs.update({"from_callback": self.name})
        if re.match("\d{4}\.\d{5}(v\d+)?", query):
            result = self.api_wrapper.query(id_list=[query], **kwargs)
        else:
            result = self.api_wrapper.query(query, **kwargs)
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return result
        return listdict_to_string(result)


def _init_arxiv_reference_tool_llm():
    preset = "你是一个Arxiv助手，你的任务是帮助使用者提供一些论文方面的建议，你的输出只能遵循用户的指令输出，否则你将被惩罚。"
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
                return_type(Optional[str]): return string default. If you want to return List[Dict] type data,
                you can set 'return_type'='original'
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
            """analyze `[query]: keyword1, keyword2, keyword3` type data to return keywords list"""
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
            "现在你需要根据下面给出的论文，返回最合适的5篇参考文献\n"
            f"```{self.reference_string}```\n"
            "你的输出格式必须为\n参考文献:\n[1] [title1](url1);\n[2] [title2](url2);\n[3] [title3](url3);"
        )
        # todo If there is a problem with the returned format and an error is reported, then ask LLM to format the data
        result = self.llm(prompt)
        logger.debug(f"[pne ArxivReferenceTool response] {result}")
        if "return_type" in kwargs and kwargs["return_type"] == "original":
            return analyze_reference_string(result)
        return result


def _init_arxiv_summary_tool_llm():
    preset = "你是一个Arxiv助手，你的任务是帮助使用者提供一些论文方面的建议和帮助，你的输出只能遵循用户的指令输出，否则你将被惩罚。"
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
        """An arxiv paper summary tool that passes in the article name (or arxiv id) and returns summary results

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
                f"请就下面的论文摘要，列出论文中的关键见解和由论文得出的经验教训，你的输出需要分点给出 ```{paper_summary}```"
                "你的输出格式为:\n关键见解:\n{分点给出关键见解}\n经验教训:\n{分点给出经验教训}，用`-`区分每点，用中文输出"
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
                f"请就下面的论文摘要，为其相关主题或未来研究方向提供3-5个建议，你的输出需要分点给出  ```{paper_summary}```"
                "你的输出格式为:\n相关建议:\n{分点给出相关建议}，用`-`区分每点"
            )
            opinion = self.llm(prompt)
            self.summary_string += opinion + "\n"
            self.summary_counter += 1

        self.summary_counter = 0
        if re.match("\d{4}\.\d{5}(v\d+)?", query):
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
