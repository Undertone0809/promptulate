import asyncio
import logging
from integration.agent import NautilusAgent
from integration.config import Config

logging.basicConfig(level=logging.INFO)

async def main():
    # 创建代理实例
    agent = NautilusAgent(
        name=Config.AGENT_NAME,
        nautilus_endpoint=Config.NAUTILUS_ENDPOINT,
        private_key=Config.PRIVATE_KEY,
        capabilities=Config.AGENT_CAPABILITIES,
        endpoint=Config.AGENT_ENDPOINT
    )

    # 注册代理
    registered = await agent.register()
    if not registered:
        print("Agent registration failed")
        return

    # 获取余额
    balance = await agent.get_balance()
    print(f"Balance: {balance} NAU")

    # 示例：发送消息给另一个代理（需要知道目标代理ID）
    # await agent.send_message("target_agent_id", "Hello from test!")

    # 运行代理主循环（会持续接收消息）
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
