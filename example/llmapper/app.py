import streamlit as st
from core import LLMResponse, create_knowledge_graph, draw_graph, read_summarize_prompt

import promptulate as pne
from promptulate.tools.wikipedia import wikipedia_search

# Create a sidebar to place the user parameter configuration
with st.sidebar:
    model_name: str = st.selectbox(
        label="Language Model Name",
        options=[
            "openai/gpt-4o",
            "openai/gpt-4-turbo",
            "deepseek/deepseek-chat",
            "zhipu/glm-4",
            "ollama/llama2",
        ],
        help="For more details, please see"
        "[how to write model name?]("
        "https://www.promptulate.cn/#/other/how_to_write_model_name)",
    )
    api_key = st.text_input("API Key", key="provider_api_key", type="password")
    api_base = st.text_input("OpenAI Proxy URL (Optional)")
    "[View the source code](https://github.com/Undertone0809/promptulate)"

# Set title
st.title("💬 Chat")
st.caption(
    "🚀 Hi there! 👋 I am a chatbot using llmapper to draw knowledge map by "
    "Promptulate to help you."
)
# Determine whether to initialize the message variable
# otherwise initialize a message dictionary
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"},
    ]
# Traverse messages in session state
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input():
    if not api_key:
        st.info("Please add your API key to continue.")
        st.stop()
    # Display the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    query_result: str = wikipedia_search(prompt, top_k_results=1)
    # display search results in the chatbot panel
    # st.chat_message("assistant").write(query_result)

    summarize_prompt_path = "prompt-summarize.md"
    summarize_prompt = read_summarize_prompt(summarize_prompt_path)
    _prompt = f"""
    Please generate a knowledge graph based on the requirements of {summarize_prompt}
    and the content of {query_result}
    """

    llm_response: LLMResponse = pne.chat(
        model=model_name,
        messages=_prompt,
        model_config={"api_base": api_base, "api_key": api_key},
        output_schema=LLMResponse,
    )
    # Display the summarized concept list in the chatbot panel
    # st.chat_message("assistant").write(str(llm_response.model_dump()))

    # generate and draw the knowledge graph
    G = create_knowledge_graph(llm_response.model_dump())
    buf = draw_graph(G)
    # Convert the graph to a base64 image and display it
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "The following is the generated knowledge map:",
        }  # noqa
    )
    st.chat_message("assistant").write("The following is the generated knowledge map:")
    st.image(buf)
