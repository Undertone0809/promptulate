import gradio as gr

import promptulate as pne

# # 定义模型选项
MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4", "deepseek/deepseek-chat"]


def predict(message, history, api_key, model, api_base):
    # Check if the API key is provided
    if not api_key:
        yield "Error: API key is required."
        return

    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})

    history_openai_format.append({"role": "user", "content": message})

    # Create model_config dictionary
    model_config = {
        "api_key": api_key,
    }
    if api_base:
        model_config["api_base"] = api_base

    response = pne.chat(
        messages=history_openai_format,
        model=model,
        stream=True,
        model_config=model_config,
    )

    partial_message = ""
    for chunk in response:
        if chunk is not None:
            partial_message = partial_message + chunk
            yield partial_message


def main():
    with gr.Blocks() as demo:
        gr.Markdown("# Promptulate Gradio Playground")
        with gr.Row():
            with gr.Column(scale=1):
                api_key = gr.Textbox(
                    label="API Key",
                    placeholder="Enter your OpenAI API key here",
                    type="password",
                )
                model_selector = gr.Dropdown(
                    label="Select Model", choices=MODEL_OPTIONS, value=MODEL_OPTIONS[0]
                )

                api_base = gr.Textbox(
                    label="API Base",
                    placeholder="Enter your OpenAI API proxy here (optional)",
                )

            with gr.Column(scale=3):
                chat_interface = gr.ChatInterface(  # noqa
                    fn=predict,
                    additional_inputs=[api_key, model_selector, api_base],
                    fill_height=True,
                )
        gr.Markdown("## Instructions")
        gr.Markdown(
            """
            1. Enter your API key.\n
            2. Select the model you want to use.\n
            3. Start chatting!\n
            4. Use the 'Clear History' button to clear the chat history.
            """
        )

    demo.launch()


if __name__ == "__main__":
    main()
