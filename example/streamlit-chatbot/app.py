import pne
import streamlit as st


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you?"}
        ]


def render_chat_history():
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


def get_user_input() -> str:
    return st.chat_input("How can I help you?")


def update_chat(role: str, content: str):
    """Update the chat history with the new message from the user or assistant."""
    st.session_state.messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)


def generate_response(model_name: str, api_base: str, api_key: str) -> str:
    """Generate a response using the specified model."""
    with st.chat_message("assistant"):
        stream = pne.chat(
            model=model_name,
            stream=True,
            messages=st.session_state.messages,
            model_config={"api_base": api_base, "api_key": api_key},
        )
        response = st.write_stream(stream)
    return response


def main():
    initialize_session_state()
    config = pne.beta.st.model_sidebar()

    st.title("💬 Chat")
    st.caption("🚀 Hi there! 👋 I am a simple chatbot by Promptulate to help you.")

    render_chat_history()

    if prompt := get_user_input():
        if not config["api_key"]:
            st.info("Please add your API key to continue.")
            st.stop()

        update_chat("user", prompt)
        generate_response(**config)


if __name__ == "__main__":
    main()
