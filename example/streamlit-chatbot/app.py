import streamlit as st

import promptulate as pne

# Create a sidebar to place the user parameter configuration
with st.sidebar:
    model_name: str = st.text_input(
        label="LLM Model Name",
        help="1.gpt-4-1106-preview "
        "2.deepseek/deepseek-chat "
        "For more details, please click ("
        "https://www.promptulate.cn/#/use_cases/chat_usage?id=chat)",
    )
    api_key = st.text_input("API Key", key="chatbot_api_key", type="password")
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

    # Stream output
    for i in response:
        st.session_state.messages.append({"role": "assistant", "content": i})
        st.chat_message("assistant").write(i)
