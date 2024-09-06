import pne
import streamlit as st
from core import PersonalHealingAssistant


def main():
    config = pne.beta.st.model_sidebar()
    # todo llm default answer with cn
    with st.sidebar:
        mem0_user_id = st.text_input("mem0 user id", type="password")
        mem_api_key = st.text_input(
            "mem0 API Key", key="provider_mem0_api_key", type="password"
        )

    st.title("PersonalHealingAssistant")
    st.caption(
        """
        Personal Healing Assistant combines pne and mem0ai to create a personalized healing assistant for you \n
        🚀 Power by [promptulate](https://github.com/Undertone0809/promptulate)
        """  # noqa
    )
    st.chat_message("assistant").write(
        "I am your personal healing assistant, how can I help you? "
    )

    ai_assistant = PersonalHealingAssistant()

    if prompt := st.chat_input("Please enter what you want to know "):
        if not config.api_key:
            st.info("Please add your model API key to continue.")
            st.stop()

        if not mem_api_key:
            st.error("Please provide your mem0 API Key to continue.")
            st.stop()

        ai_assistant.set_mem_api_key(mem_api_key)

        answer = ai_assistant.ask_question(
            question=prompt, user_id=mem0_user_id, config=config
        )

        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write_stream(answer)


if __name__ == "__main__":
    main()
