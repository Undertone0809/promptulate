import logging
import sys
from nautilus_client import NautilusClient
from agent_infrastructure import PromptulateNautilusAgent

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """测试集成功能的主函数"""
    # 配置参数（实际使用时请替换为真实值）
    NAUTILUS_BASE_URL = "https://api.nautilus.example.com"  # 替换为实际URL
    API_KEY = "your_api_key_here"  # 替换为实际API密钥
    
    # 初始化Nautilus客户端
    client = NautilusClient(NAUTILUS_BASE_URL, API_KEY)
    
    # 创建两个测试代理
    agent1 = PromptulateNautilusAgent(
        agent_id="agent_test_1",
        nautilus_client=client,
        capabilities=["text_processing", "data_analysis"],
        name="TestAgent1"
    )
    agent2 = PromptulateNautilusAgent(
        agent_id="agent_test_2",
        nautilus_client=client,
        capabilities=["image_processing"],
        name="TestAgent2"
    )
    
    # 注册代理
    logger.info("Registering agent1...")
    if not agent1.register_on_nautilus():
        logger.error("Failed to register agent1")
        sys.exit(1)
    logger.info("Registering agent2...")
    if not agent2.register_on_nautilus():
        logger.error("Failed to register agent2")
        sys.exit(1)
    
    # 查询代理信息
    info1 = client.get_agent_info("agent_test_1")
    if info1:
        logger.info(f"Agent1 info: {info1}")
    else:
        logger.warning("Could not fetch agent1 info")
    
    # 发送A2A消息
    logger.info("Sending A2A message from agent1 to agent2...")
    message = {"id": "msg_001", "content": "Hello from agent1", "timestamp": "2025-01-01T00:00:00Z"}
    response = agent1.send_message_to_agent("agent_test_2", message)
    if response:
        logger.info(f"A2A response: {response}")
    else:
        logger.error("A2A message failed")
    
    # 模拟接收消息（实际中由平台回调）
    agent2.receive_message("agent_test_1", message)
    
    # 代币转移
    logger.info("Transferring 10 NAU from agent1 to agent2...")
    if agent1.transfer_tokens("agent_test_2", 10.0):
        logger.info("Token transfer successful")
    else:
        logger.error("Token transfer failed")
    
    # 查询余额
    balance1 = agent1.get_balance()
    balance2 = agent2.get_balance()
    logger.info(f"Agent1 balance: {balance1}")
    logger.info(f"Agent2 balance: {balance2}")
    
    # 执行任务
    result = agent1.run("Analyze data")
    logger.info(f"Task result: {result}")
    
    # 清理
    client.close()
    logger.info("Test completed successfully")

if __name__ == "__main__":
    main()