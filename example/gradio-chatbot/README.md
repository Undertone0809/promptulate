# Build a gradio+ pne.chat simple chat app 

The `chat.py` is an example of building a gradio+ pne.chat simple chat app .

# Quick Start

1. Clone the repository and install the dependencies

   ```shell
   git clone https://www.github.com/Undertone0809/promptulate
   cd ./example/gradio-chatbot
   pip install -r requirements.txt
   ```

2. Configure environment variables

   ```shell
   echo OPENAI_API_KEY="your_openai_api_key" > .env
   ```

   You can also configure environment variables directly in the program.

   ```python
   import os
   os.environ["OPENAI_API_KEY="] = "your_openai_api_key"
   ```

3. Run the application

   ```shell
   python chat.py
   ```

   

