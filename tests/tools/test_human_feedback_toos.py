from promptulate.tools.human_feedback import HumanFeedBackTool


def output_func(llm_question: str):
    print(llm_question)


def input_func():
    return "human_answer"


def test_human_fb_tool():
    tool = HumanFeedBackTool(output_func=output_func, input_func=input_func)
    answer = tool.run("Hello")
    assert answer == "human_answer"
