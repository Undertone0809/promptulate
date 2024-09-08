<script setup>
import IFrame from '/components/iframe.vue'
</script>

# Build a chatbot using gradio

This demo shows how to use `pne.chat()` to create a simple chatbot utilizing any model. For the application frontend, we will be using gradio, an easy-to-use open-source Python framework.

This application serves as a template, meaning you can create your own LLM application based on this template.

You can try the live demo at [https://huggingface.co/spaces/Zeeland2hf/pne-gradio](https://huggingface.co/spaces/Zeeland2hf/pne-gradio) or see the code [here]().

<IFrame src="https://zeeland2hf-pne-gradio.hf.space" />

## Prerequisites
    
Before you start, ensure you have Python installed on your system. You will also need the following Python packages:
- `gradio`
- `pne` 

You can install these packages using pip:

```bash
pip install gradio pne
```

## Code Overview

The following sections explain the key components of the code.

### 1. Import Libraries

First, import the necessary libraries:

```python
import gradio as gr
import pne
```

### 2. Define Model Options

Specify the available models:

```python
MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4"]
```

### 3. Define the Prediction Function

The `predict` function handles the chat logic, interacting with the OpenAI API based on user input and chat history:

```python
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
```

### 4. Build the Gradio Interface

Create the Gradio interface, including input fields for the API key, model selection, and optional API base URL:

```python
def main():
    with gr.Blocks() as demo:
        gr.Markdown("# Promptulate + Gradio Demo")
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
                    label="API Base", placeholder="Enter your OpenAI API base here (optional)"
                )

            with gr.Column(scale=3):
                chat_interface = gr.ChatInterface(
                    fn=predict,
                    additional_inputs=[api_key, model_selector, api_base],
                    fill_height=True,
                )
        gr.Markdown("## Instructions")
        gr.Markdown(
            "1. Enter your OpenAI API key.\n2. Select the model you want to use.\n3. Start chatting!\n4. Use the 'Clear History' button to clear the chat history."
        )

    demo.launch(share=True)
```

### 5. Run the Application

Use the `main` function to launch the Gradio app:

```python
if __name__ == "__main__":
    main()
```

## Complete Code

Here's the complete code for easy reference:

```python
import gradio as gr
import pne

# Define model options
MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4"]

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
        gr.Markdown("# Promptulate + Gradio Demo")
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
                    label="API Base", placeholder="Enter your OpenAI API base here (optional)"
                )

            with gr.Column(scale=3):
                chat_interface = gr.ChatInterface(
                    fn=predict,
                    additional_inputs=[api_key, model_selector, api_base],
                    fill_height=True,
                )
        gr.Markdown("## Instructions")
        gr.Markdown(
            "1. Enter your OpenAI API key.\n2. Select the model you want to use.\n3. Start chatting!\n4. Use the 'Clear History' button to clear the chat history."
        )

    demo.launch(share=True)

if __name__ == "__main__":
    main()
```

## Running the Application

To run the application, save the code to a file (e.g., `chat.py`) and execute it:

```bash
python app.py
```

This will launch the Gradio app, and you will receive a URL to access the chatbot in your browser.

## Example Screenshot

Here demonstrate the working chatbot interface.

![image-20240716175616736](.\img\pne.chat()+gradio.png)

By following these instructions, you can easily set up and run your own chatbot using `pne` and `gradio`. Enjoy chatting!