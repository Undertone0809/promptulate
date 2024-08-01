import pandas as pd
import streamlit as st
from loguru import logger
from repo_service import RepoManager
from token_count import num_messages, num_tokens_from_string

import promptulate as pne


class StreamHandler:
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def process_token(self, token: str):
        if not isinstance(token, str):
            token = str(token)
        self.text += token
        self.container.markdown(self.text)


def refresh_repos():
    logger.info("Refreshing repositories")
    if "repoManager" not in st.session_state:
        st.session_state["repoManager"] = RepoManager()
    st.session_state["repoManager"].load_repos()
    st.success("Refreshed repositories")


def create_app():
    st.set_page_config(page_title="ChatWithRepo", page_icon="🤖")

    if "repoManager" not in st.session_state:
        st.session_state["repoManager"] = RepoManager()
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    repoManager: RepoManager = st.session_state["repoManager"]
    with st.sidebar:
        st.title("Settings for Repo")
        custom_repo_url = st.text_input("Custom Repository URL")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add Custom Repository"):
                if repoManager.add_repo(custom_repo_url):
                    st.success(f"Added custom repository: {custom_repo_url}")
                else:
                    st.error(f"Repository add failed: {custom_repo_url}")
                repo_url = custom_repo_url
        with col2:
            if st.button("Refresh Repositories"):
                refresh_repos()

        repo_url = st.selectbox("Repository URL", options=repoManager.get_repo_urls())
        if repoManager.check_if_repo_exists(repo_url):
            repo = repoManager.get_repo_service(repo_url)
            selected_folder = st.multiselect(
                "Select Folder", options=repo.get_folders_options()
            )
            selected_files = st.multiselect(
                "Select Files", options=repo.get_files_options(), default="README.md"
            )
            selected_languages = st.multiselect(
                "Filtered by Language", options=repo.get_languages_options()
            )
            limit = st.number_input("Limit", value=100000, step=10000)
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Count Tokens"):
                    file_string = repo.get_filtered_files(
                        selected_folders=selected_folder,
                        selected_files=selected_files,
                        selected_languages=selected_languages,
                        limit=limit,
                    )
                    st.write(f"Total Tokens: {num_tokens_from_string(file_string)}")
            with col2:
                if st.button("Update Repo"):
                    if repo.update_repo():
                        st.success(f"Updated repository: {repo_url}")
                    else:
                        st.error(f"Repository update failed: {repo_url}")
                    st.rerun()
            with col3:
                if st.button("Delete Repo"):
                    if repo.delete_repo():
                        st.success(f"Deleted repository: {repo_url}")
                    else:
                        st.error(f"Repository delete failed: {repo_url}")
                    refresh_repos()
                    st.rerun()

        st.title("Settings for LLM")

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

        selected_model = st.selectbox(
            label="Language Model Name", options=model_options
        )

        model_name = selected_model
        if selected_model == "Custom Model":
            # Show a text input field for custom model name when "Custom Model" is
            # selected
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
        temperature = st.slider(
            "Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1
        )
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a helpful assistant. You are provided with a repo "
            "information and files from the repo. Answer the user's questions "
            "based on the information and files provided.",
        )

        if st.button("Clear Chat"):
            st.session_state["messages"] = []

    if repoManager.isEmpty():
        st.info("Copy the repository URL and click the download button.")
        st.stop()

    if not repoManager.check_if_repo_exists(repo_url):
        st.info(f"{repo_url} does not exist. Please add the repository first.")
        st.stop()

    repo = repoManager.get_repo_service(repo_url)
    st.title(f"Repo: {repo.repo_name}")
    st.write(
        "Chat with LLM using the repository information and files. You can change "
        "model settings anytime during the chat."
    )
    st.info(
        f"""
    Files : {selected_files}
    Folder: {selected_folder}
    Languages: {selected_languages}
    Limit: {limit}
    """
    )
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        logger.info(f"User: {prompt}, received at {pd.Timestamp.now()}")

        start_time = pd.Timestamp.now()
        # Check if the selected model has changed
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = None

        if st.session_state.selected_model != selected_model:
            st.session_state.selected_model = selected_model

        file_string = repo.get_filtered_files(
            selected_folders=selected_folder,
            selected_files=selected_files,
            selected_languages=selected_languages,
            limit=limit,
        )
        end_time = pd.Timestamp.now()
        logger.info(f"Time taken to get filtered files: {end_time - start_time}")

        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            # only add file content to the system prompt
            messages = (
                [{"role": "system", "content": system_prompt}]
                + [{"role": "user", "content": file_string}]
                + st.session_state.messages
            )

            # log the information
            total_tokens = num_messages(messages)
            logger.info(
                f"Information: {selected_files}, {selected_folder}, {selected_languages}"  # noqa
            )
            logger.info(f"Using settings: {selected_model}, {temperature}")
            logger.info(f"File token: {num_tokens_from_string(file_string)}")
            logger.info(f"Total Messages Token: {total_tokens}")
            st.sidebar.write(
                f"Sending file content: {selected_files} and filter folder: {selected_folder} to the assistant."  # noqa
            )
            st.sidebar.write(f"total messages token: {total_tokens}")

            # send to llm
            response = pne.chat(
                model=model_name,
                stream=True,
                messages=messages,
                model_config={"api_base": api_base, "api_key": api_key},
            )

            for chunk in response:
                content = chunk
                stream_handler.process_token(content)

            st.session_state.messages.append(
                {"role": "assistant", "content": stream_handler.text}
            )


if __name__ == "__main__":
    create_app()
