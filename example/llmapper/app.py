import streamlit as st
from core import (
    AppConfig,
    Graph,
    create_knowledge_graph,
    draw_graph,
    generate_nodes,
)

from promptulate.tools.wikipedia import wikipedia_search


def main():
    app_config = AppConfig()
    with st.sidebar:
        app_config.model_name = st.selectbox(
            label="Language Model Name",
            options=[
                "openai/gpt-4o",
                "openai/gpt-4-turbo",
                "deepseek/deepseek-chat",
                "zhipu/glm-4",
                "ollama/llama2",
            ],
            help="For more details, please see"
            "[how to write model name?]("
            "https://www.promptulate.cn/#/other/how_to_write_model_name)",
        )
        app_config.api_key = st.text_input(
            "API Key", key="provider_api_key", type="password"
        )
        app_config.api_base = st.text_input("OpenAI Proxy URL (Optional)")
        "[View the source code](https://github.com/Undertone0809/promptulate)"

    st.title("llmapper")
    st.caption(
        """
        LLMapper was an experimental project. Given a query term, llmapper would search Wikipedia for relevant content, and then generate a knowledge graph using Promptulate.\n
        🚀 Power by [promptulate](https://github.com/Undertone0809/promptulate)
        """  # noqa
    )
    st.chat_message("assistant").write(
        "Input the query you want to generate a knowledge graph for."
    )

    if prompt := st.chat_input():
        if not app_config.api_key:
            st.info("Please add your API key to continue.")
            st.stop()

        st.chat_message("user").write(prompt)

        st.chat_message("assistant").write(f"Querying {prompt} from Wikipedia...")

        query_result: str = wikipedia_search(prompt, top_k_results=1)

        st.chat_message("assistant").write(
            f"Found the following content from Wikipedia:\n{query_result}"
        )
        st.chat_message("assistant").write(
            "Generating knowledge graph based on the query result..."
        )

        graph: Graph = generate_nodes(query_result, app_config)

        # generate and draw the knowledge graph
        G = create_knowledge_graph(graph)
        buf = draw_graph(G)

        st.chat_message("assistant").write(
            "The following is the generated knowledge map:"
        )
        st.image(buf)


if __name__ == "__main__":
    main()
