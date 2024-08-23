from typing import Any, Callable, Dict, List, Optional


class ModelConfig:
    def __init__(
        self, model_name: str, api_key: str, api_base: Optional[str] = None, **kwargs
    ):
        self.model_name: str = model_name
        self.api_key: str = api_key
        self.api_base: Optional[str] = api_base
        self.__dict__.update(kwargs)


def model_sidebar(
    model_options: Optional[List[str]] = None,
    additional_sidebar_fn: Optional[Callable[[], Dict[str, Any]]] = None,
) -> ModelConfig:
    import streamlit as st

    model_options = model_options or [
        "Custom Model",
        "openai/gpt-4o",
        "openai/gpt-4o-mini",
        "openai/gpt-4-turbo",
        "deepseek/deepseek-chat",
        "claude-3-5-sonnet-20240620",
        "zhipu/glm-4",
        "ollama/llama2",
        "groq/llama-3.1-70b-versatile",
    ]

    with st.sidebar:
        selected_model = st.selectbox("Language Model Name", model_options)

        if selected_model == "Custom Model":
            selected_model = st.text_input(
                "Enter Custom Model Name",
                placeholder="Custom model name, eg: groq/llama3-70b-8192",
                help="For more details, please see [how to write model name?](https://www.promptulate.cn/#/other/how_to_write_model_name)",  # noqa
            )

        api_key = st.text_input("API Key", key="provider_api_key", type="password")
        api_base = st.text_input("OpenAI Proxy URL (Optional)")
        additional_config = {}

        if additional_sidebar_fn:
            additional_config: dict = additional_sidebar_fn()

    return ModelConfig(
        model_name=selected_model,
        api_key=api_key,
        api_base=api_base,
        **additional_config,
    )
