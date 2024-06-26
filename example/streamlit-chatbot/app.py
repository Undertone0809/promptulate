import pne
import streamlit as st

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
        "[how to write model name?](https://www.promptulate.cn/#/other/how_to_write_model_name)",  # noqa
    )
    api_key = st.text_input("API Key", key="provider_api_key", type="password")
    api_base = st.text_input("OpenAI Proxy URL (Optional)")

# Set title
st.title("💬 Chat")
st.caption("🚀 Hi there! 👋 I am a simple chatbot by Promptulate to help you.")

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
    if not api_key:
        st.info("Please add your API key to continue.")
        st.stop()

    # Add the message entered by the user to the list of messages in the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display in the chat interface
    st.chat_message("user").write(prompt)

    response: str = pne.chat(
        model=model_name,
        stream=True,
        messages=prompt,
        model_config={"api_base": api_base, "api_key": api_key},
    )

    st.session_state.messages.append({"role": "assistant", "content": "start"})
    st.chat_message("assistant").write_stream(response)
