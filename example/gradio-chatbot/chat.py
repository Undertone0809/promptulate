import promptulate as pne
import gradio as gr


def predict(message, history):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human})
        history_openai_format.append({"role": "assistant", "content": assistant})

    history_openai_format.append({"role": "user", "content": message})
    response = pne.chat(
        messages=history_openai_format,
        model="gpt-3.5-turbo",
        stream=True,
    )
    partial_message = ""
    for chunk in response:
        if chunk is not None:
            partial_message = partial_message + chunk
            yield partial_message


def main():
    gr.ChatInterface(
        predict,
    ).launch()


if __name__ == "__main__":
    main()
