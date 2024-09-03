import pne
import streamlit as st
from core import PersonalHealingAssistant


def main():
    config = pne.beta.st.model_sidebar()

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
            st.info("Please add your API key to continue.")
            st.stop()

        answer = ai_assistant.ask_question(
            question=prompt, user_id="hizeros", config=config
        )

        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write_stream(answer)


if __name__ == "__main__":
    main()
