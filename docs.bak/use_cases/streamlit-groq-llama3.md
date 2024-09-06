# Groq, llama3, Streamlit to build a application
This demo is how to use promptulate chat to create a simple chatbot utilising Groq and llama3 model. 

For the application frontend, there will be using streamlit, an easy-to-use open-source Python framework. 

You see try the live demo [here](https://pne-groq-chatbot.streamlit.app/) or see the code [here](https://github.com/Undertone0809/promptulate/tree/main/example/streamlit-groq-llama3-chatbot).

## Environment Setup

We can start off by creating a new conda environment with python=3.11:`conda create -n streamlit_groq_chatbot python=3.11`

Activate the environment:`conda activate streamlit_groq_chatbot`

Next, let’s install all necessary libraries:

```shell
pip install -U promptulate streamlit
```

## Step-by-Step Implementation 

### Step 1

Create a `app.py` script and import the necessary dependencies:

```python
import streamlit as st

import promptulate as pne
```

### Step 2
Create a sidebar to place the user parameter configuration:

```python
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", key="chatbot_api_key", type="password")
```

### Step 3 
Set page style:

```python
# Set title
st.title("💬 Chat")
st.caption("🚀 Hi there! 👋 I am a simple chatbot by groq and llama3 to help you ")

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
# User input
if prompt := st.chat_input():
    if not groq_api_key:
        st.info("Please add your Groq API key to continue.")
        st.stop()

    # Add the message entered by the user to the list of messages in the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display in the chat interface
    st.chat_message("user").write(prompt)

    response: str = pne.chat(
        model="groq/llama3-8b-8192",
        messages=prompt,
        model_config={"api_key": groq_api_key},
    )

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
```

## Effect
The running effect is as follows:
![streamlit+groq+llama3](./img/streamlit-groq-llama3.png)

## Demo
There is a `app.py` file under the `streamlit-chatbot` file of `example` in the project folder. 
You can run the application directly to view the effect and debug the web page. 
Project Link: [streamlit-groq-llama3](https://github.com/Undertone0809/promptulate/tree/main/example/streamlit-groq-llama3-chatbot)
To run the application, follow the steps below:

- Click [here](https://github.com/Undertone0809/promptulate/fork) to fork the project to your local machine
- Clone the project locally:

```bash
git clone https://github.com/Undertone0809/promptulate.git
```

- Switch the current directory to the example

```shell
cd ./example/streamlit-groq-llama3-chatbot
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
![streamlit+groq+llama3](./img/streamlit-groq-llama3.png)