import pne
import streamlit as st


def main():
    with st.sidebar:
        model_options = [
            "openai/gpt-4o",
            "openai/gpt-4-turbo",
            "deepseek/deepseek-chat",
            "zhipu/glm-4",
            "ollama/llama2",
            "groq/llama-3.1-70b-versatile",
            "claude-3-5-sonnet-20240620",
        ]

        # Add a placeholder for custom model name entry
        model_options.insert(0, "Custom Model")

        selected_option = st.selectbox(
            label="Language Model Name",
            options=model_options,
        )

        model_name = selected_option
        if selected_option == "Custom Model":
            model_name = st.text_input(
                "Enter Custom Model Name",
                placeholder="Custom model name, eg: groq/llama3-70b-8192",
                help=(
                    "For more details, please see "
                    "[how to write model name?](https://www.promptulate.cn/#/other/how_to_write_model_name)"  # noqa
                ),
            )
        api_key = st.text_input("API Key", key="provider_api_key", type="password")
        api_base = st.text_input("OpenAI Proxy URL (Optional)")

    st.title("💬 Chat")
    st.caption("🚀 Hi there! 👋 I am a simple chatbot by Promptulate to help you.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("How can I help you?"):
        if not api_key:
            st.info("Please add your API key to continue.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = pne.chat(
                model=model_name,
                stream=True,
                messages=st.session_state.messages,
                model_config={"api_base": api_base, "api_key": api_key},
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
