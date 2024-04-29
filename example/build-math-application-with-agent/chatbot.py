import streamlit as st

import promptulate as pne
from promptulate.hook import Hook, HookTable
from promptulate.llms import ChatOpenAI
from promptulate.tools.math.tools import calculator
from promptulate.tools.wikipedia.tools import wikipedia_search


class MidStepOutHook:
    @staticmethod
    def handle_agent_revise_plan(*args, **kwargs):
        messages = f"[Revised Plan] {kwargs['revised_plan']}"
        st.chat_message("assistant").write(messages)

    @staticmethod
    def handle_agent_action(*args, **kwargs):
        messages = f"[Thought] {kwargs['thought']}\n"
        messages += f"[Action] {kwargs['action']} args: {kwargs['action_input']}"
        st.chat_message("assistant").write(messages)

    @staticmethod
    def handle_agent_observation(*args, **kwargs):
        messages = f"[Observation] {kwargs['observation']}"
        st.chat_message("assistant").write(messages)

    @staticmethod
    def registry_hooks():
        """Registry and enable stdout hooks. StdoutHook can print colorful
        information."""
        Hook.registry_hook(
            HookTable.ON_AGENT_REVISE_PLAN,
            MidStepOutHook.handle_agent_revise_plan,
            "component",
        )
        Hook.registry_hook(
            HookTable.ON_AGENT_ACTION, MidStepOutHook.handle_agent_action, "component"
        )
        Hook.registry_hook(
            HookTable.ON_AGENT_OBSERVATION,
            MidStepOutHook.handle_agent_observation,
            "component",
        )


def build_agent(api_key: str) -> pne.ToolAgent:
    MidStepOutHook.registry_hooks()

    # calculator tool for arithmetics
    def math_tool(expression: str):
        """Useful for when you need to answer questions about math. This tool is only
        for math questions and nothing else. Only input math expressions.

        Args:
            expression: A mathematical expression, eg: 18^0.43

        Attention:
            Expressions can not exist variables!
            eg: (current age)^0.43 is wrong, you should use 18^0.43 instead.

        Returns:
            The result of the evaluation.
        """
        return calculator(expression)

    # reasoning based tool
    def word_problem_tool(question: str) -> str:
        """
        Useful for when you need to answer logic-based/reasoning questions.

        Args:
            question(str): Detail question, the description of the problem requires a
            detailed question context. Include a description of the problem

        Returns:
            question answer
        """
        system_prompt: str = """You are a reasoning agent tasked with solving t he user's logic-based questions.
        Logically arrive at the solution, and be factual.
        In your answers, clearly detail the steps involved and give the final answer.
        Provide the response in bullet points."""  # noqa
        llm = ChatOpenAI(private_api_key=api_key)
        return llm(f"{system_prompt}\n\nQuestion:{question}Answer:")

    # Wikipedia Tool
    def wikipedia_tool(keyword: str) -> str:
        """search by keyword in web.

        A useful tool for searching the Internet to find information on world events,
        issues, dates,years, etc. Worth using for general topics. Use precise questions.

        Args:
            keyword: keyword to search

        Returns:
            str: search result
        """
        return wikipedia_search(keyword)

    llm = ChatOpenAI(model="gpt-4-1106-preview", private_api_key=api_key)
    return pne.ToolAgent(tools=[wikipedia_tool, math_tool, word_problem_tool], llm=llm)


# Create a sidebar to place the user parameter configuration
with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"  # noqa

# Set title
st.title("💬 Math Wiz")
st.caption(
    "🚀 Hi there! 👋 I am a reasoning tool by Promptulate to help you "
    "with your math or logic-based reasoning questions."
)

# Determine whether to initialize the message variable
# otherwise initialize a message dictionary
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

# Traverse messages in session state
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    agent: pne.ToolAgent = build_agent(api_key=openai_api_key)

    # Add the message entered by the user to the list of messages in the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display in the chat interface
    st.chat_message("user").write(prompt)

    response: str = agent.run(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
