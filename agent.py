import asyncio
import logging
from typing import Optional, Dict, Any
from promptulate import Agent
from nautilus_sdk import NautilusClient, AgentRegistration, Message, TokenTransaction

logger = logging.getLogger(__name__)

class NautilusAgent(Agent):
    """集成Nautilus的Promptulate代理"""

    def __init__(self, name: str, nautilus_endpoint: str, private_key: str, **kwargs):
        super().__init__(name=name, **kwargs)
        self.nautilus_client = NautilusClient(endpoint=nautilus_endpoint, private_key=private_key)
        self.agent_id: Optional[str] = None
        self.registration: Optional[AgentRegistration] = None

    async def register(self) -> bool:
        """在Nautilus平台注册代理"""
        try:
            self.registration = AgentRegistration(
                name=self.name,
                capabilities=self.capabilities,
                endpoint=self.endpoint
            )
            response = await self.nautilus_client.register_agent(self.registration)
            if response.status == 'success':
                self.agent_id = response.agent_id
                logger.info(f"Agent {self.name} registered with ID {self.agent_id}")
                return True
            else:
                logger.error(f"Registration failed: {response.message}")
                return False
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False

    async def send_message(self, target_agent_id: str, content: str) -> bool:
        """通过Nautilus A2A网关发送消息"""
        try:
            message = Message(
                sender_id=self.agent_id,
                receiver_id=target_agent_id,
                content=content
            )
            response = await self.nautilus_client.send_message(message)
            if response.status == 'success':
                logger.info(f"Message sent to {target_agent_id}")
                return True
            else:
                logger.error(f"Send message failed: {response.message}")
                return False
        except Exception as e:
            logger.error(f"Send message error: {e}")
            return False

    async def receive_messages(self) -> list:
        """接收来自其他代理的消息"""
        try:
            messages = await self.nautilus_client.get_messages(self.agent_id)
            return messages
        except Exception as e:
            logger.error(f"Receive messages error: {e}")
            return []

    async def transfer_tokens(self, to_agent_id: str, amount: float) -> bool:
        """向其他代理转移NAU代币"""
        try:
            transaction = TokenTransaction(
                from_agent_id=self.agent_id,
                to_agent_id=to_agent_id,
                amount=amount
            )
            response = await self.nautilus_client.transfer_tokens(transaction)
            if response.status == 'success':
                logger.info(f"Transferred {amount} NAU to {to_agent_id}")
                return True
            else:
                logger.error(f"Transfer failed: {response.message}")
                return False
        except Exception as e:
            logger.error(f"Transfer error: {e}")
            return False

    async def get_balance(self) -> float:
        """查询代理的NAU代币余额"""
        try:
            balance = await self.nautilus_client.get_balance(self.agent_id)
            return balance
        except Exception as e:
            logger.error(f"Get balance error: {e}")
            return 0.0

    async def run(self):
        """代理主循环"""
        await self.register()
        if not self.agent_id:
            logger.error("Agent not registered, exiting")
            return
        while True:
            messages = await self.receive_messages()
            for msg in messages:
                # 处理消息的逻辑，这里简单打印
                logger.info(f"Received message from {msg.sender_id}: {msg.content}")
                # 示例：回复消息
                await self.send_message(msg.sender_id, f"Echo: {msg.content}")
            await asyncio.sleep(1)
