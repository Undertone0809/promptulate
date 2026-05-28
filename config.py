class Config:
    """配置类，包含Nautilus连接参数"""
    NAUTILUS_ENDPOINT = "https://nautilus.example.com/api"
    PRIVATE_KEY = "your_private_key_here"
    AGENT_NAME = "MyPromptulateAgent"
    AGENT_CAPABILITIES = ["text_processing", "data_analysis"]
    AGENT_ENDPOINT = "http://localhost:8080/webhook"
