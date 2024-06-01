import streamlit as st

import promptulate as pne

# Create a sidebar to place the user parameter configuration
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", key="chatbot_api_key", type="password")

# Set title
st.title("💬 Chat")
st.caption("🚀 Hi there! 👋 I am a simple chatbot by groq and llama3 to help you ")

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
    if not groq_api_key:
        st.info("Please add your Groq API key to continue.")
        st.stop()

    # Add the message entered by the user to the list of messages in the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display in the chat interface
    st.chat_message("user").write(prompt)

    response: str = pne.chat(
        model="groq/llama3-8b-8192",
        messages=prompt,
        model_config={"api_key": groq_api_key},
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
    st.chat_message("assistant").write(response)
