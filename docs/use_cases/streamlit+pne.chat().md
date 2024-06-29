# Build a simple chatbot using streamlit and pne

This demo is how to use `pne.chat()` to create a simple chatbot utilising any model. For the application frontend, there will be using streamlit, an easy-to-use open-source Python framework. 

This application is a template, meaning you can create your own LLM application by this template.

You see try the live demo [here](https://pne-chatbot.streamlit.app/) or see the code [here](https://github.com/Undertone0809/promptulate/tree/main/example/streamlit-chatbot).

## Environment Setup

Now, let's install all necessary libraries:

```bash
pip install -U pne streamlit`
```

## Step-by-Step Implementation 

### Step 1

Create a `app.py` script and import the necessary dependencies:

```python
import pne
import streamlit as st
```

### Step 2

Create a sidebar to place the user parameter configuration:

```python
with st.sidebar:
    model_name: str = st.selectbox(
        label="Language Model Name",
        options=[
            "openai/gpt-4o",
            "openai/gpt-4-turbo",
            "deepseek/deepseek-chat",
            "zhipu/glm-4",
            "ollama/llama2",
        ],
        help="For more details, please see"
        "[how to write model name?](https://www.promptulate.cn/#/other/how_to_write_model_name)",  # noqa
    )
    api_key = st.text_input("API Key", key="provider_api_key", type="password")
    api_base = st.text_input("OpenAI Proxy URL (Optional)")

```

### Step 3 

Set page style:

```python
# Set title
st.title("💬 Chat")
st.caption("🚀 Hi there! 👋 I am a simple chatbot by Promptulate to help you.")

# Determine whether to initialize the message variable
# otherwise initialize a message dictionary
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

# Traverse messages in session state
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
```

### Step 4

Set user input:

```python
if prompt := st.chat_input():
    if not api_key:
        st.info("Please add your API key to continue.")
        st.stop()

    # Add the message entered by the user to the list of messages in the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display in the chat interface
    st.chat_message("user").write(prompt)

    response: str = pne.chat(
        model=model_name,
        stream=True,
        messages=prompt,
        model_config={"api_base": api_base, "api_key": api_key},
    )

    st.session_state.messages.append({"role": "assistant", "content": "start"})
    st.chat_message("assistant").write_stream(response)
```

## Final Effect

The running effect is as follows, you can interact with the chatbot:

![streamlit+pne](./img/streamlit+pne.png)

## How to write model name?

You can see how to write model name here: [Link](/other/how_to_write_model_name#how-to-write-model-name)

## Run the demo

There is a `app.py` file under the `streamlit-chatbot` file of `example` in the project folder. You can run the application directly to view the effect and debug the web page.

To run the application, follow the steps below:

- Click [here](https://github.com/Undertone0809/promptulate/fork) to fork the project to your local machine
- Clone the project locally:

```bash
git clone https://github.com/Undertone0809/promptulate.git
```

- Switch the current directory to the example

```shell
cd ./example/streamlit-chatbot
```

- Install the dependencies

```shell
pip install -r requirements.txt
```

- Run the application

```shell
streamlit run app.py
```

The running result is as follows:

![streamlit+pne](./img/streamlit+pne.png)