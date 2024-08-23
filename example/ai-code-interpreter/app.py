import base64
import os
import re
from io import BytesIO
from typing import Optional

import pne
import streamlit as st
from e2b_code_interpreter import CodeInterpreter
from prompt import system_prompt


def extract_code(text) -> list:
    pattern = r"```python\n(.*?)\n```"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def render_model() -> dict:
    e2b_key = st.text_input("E2B Key")
    return {"e2b_key": e2b_key}


def handle_code_block(
    code: str, config, code_interpreter: Optional[CodeInterpreter] = None
):
    code_interpreter = code_interpreter or CodeInterpreter()
    max_retries = 3
    retry_count = 0

    st.write("Running code:")
    st.code(code, language="python")

    while retry_count < max_retries:
        exec = code_interpreter.notebook.exec_cell(code)

        if exec.logs:
            st.write("Run Logs:")
            st.text(exec.logs)

        if exec.error:
            error_message = f"An error occurred: {exec.error}"
            st.error(error_message)

            error_response = pne.chat(
                model=config.model_name,
                messages=[
                    *st.session_state.messages,
                    {
                        "role": "assistant",
                        "content": "I encountered an error while executing the code.",
                    },
                    {
                        "role": "user",
                        "content": f"The code execution resulted in an error: {error_message}. Can you explain what went wrong and provide a corrected version of the code?",  # noqa
                    },
                ],
                model_config={
                    "api_base": config.api_base,
                    "api_key": config.api_key,
                },
            )

            # st.write("Let me help you fix that eror:")
            st.write(error_response)

            corrected_code_blocks = extract_code(error_response)
            if corrected_code_blocks:
                code = corrected_code_blocks[0]
                st.write("Corrected code:")
                st.code(code, language="python")

            retry_count += 1
        else:
            st.success("Code executed successfully!")
            for output in exec.results:
                if output.png:
                    image = BytesIO(base64.b64decode(output.png))
                    st.image(image)
                elif output.text:
                    st.text(output.text)
            break

    if retry_count == max_retries:
        st.error(
            f"Failed to execute the code after {max_retries} attempts. Please review the code and try again."  # noqa
        )


def additional_config() -> dict:
    e2b_api_key = st.text_input("E2B API Key")
    return {"e2b_api_key": e2b_api_key}


def main():
    st.set_page_config(layout="wide")
    config = pne.beta.st.model_sidebar(additional_sidebar_fn=additional_config)
    os.environ["E2B_API_KEY"] = config.e2b_api_key

    st.title("💬 Code-Interpreter")
    st.caption(
        "🚀 Code-Interpreter is a tool that helps you run Python code snippets in your chat messages."  # noqa
    )

    # Initialize session state
    if "show_code_results" not in st.session_state:
        st.session_state.show_code_results = False
    if "code_blocks" not in st.session_state:
        st.session_state.code_blocks = []

    # Create a layout with a dynamic right column
    left_col, right_col = st.columns([2, 1])

    with left_col:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {
                    "role": "assistant",
                    "content": system_prompt,
                }
            ]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("How can I help you?"):
            if not config.api_key:
                st.info("Please add your API key to continue.")
                st.stop()

            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            stream = pne.chat(
                model=config.model_name,
                stream=True,
                messages=st.session_state.messages,
                model_config={"api_base": config.api_base, "api_key": config.api_key},
            )
            response = st.chat_message("assistant").write_stream(stream)

            st.session_state.code_blocks = extract_code(response)

            if st.session_state.code_blocks:
                st.session_state.show_code_results = True
                st.chat_message("assistant").write(
                    f"Found {len(st.session_state.code_blocks)} code blocks."
                )

            st.session_state.messages.append({"role": "assistant", "content": response})

    if st.session_state.code_blocks:
        st.button(
            "Toggle Code Results",
            on_click=lambda: setattr(
                st.session_state,
                "show_code_results",
                not st.session_state.show_code_results,
            ),
        )

    if st.session_state.show_code_results:
        with right_col:
            st.header("Code Execution Results")
            with CodeInterpreter() as interpreter:
                for code in st.session_state.code_blocks:
                    handle_code_block(code, config, interpreter)


if __name__ == "__main__":
    main()
