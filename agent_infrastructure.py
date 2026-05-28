import logging
from typing import Dict, Any, Optional, List
from promptulate import Agent, Tool
from nautilus_client import NautilusClient

logger = logging.getLogger(__name__)

class PromptulateNautilusAgent(Agent):
    """集成Nautilus平台的promptulate代理"""
    
    def __init__(self, agent_id: str, nautilus_client: NautilusClient, capabilities: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.agent_id = agent_id
        self.nautilus = nautilus_client
        self.capabilities = capabilities or []
        self.registered = False
    
    def register_on_nautilus(self, metadata: Dict[str, Any] = None) -> bool:
        """在Nautilus平台注册当前代理"""
        if self.registered:
            logger.warning(f"Agent {self.agent_id} already registered")
            return True
        meta = metadata or {}
        meta.setdefault('name', self.agent_id)
        meta.setdefault('type', 'promptulate')
        success = self.nautilus.register_agent(self.agent_id, self.capabilities, meta)
        if success:
            self.registered = True
        return success
    
    def send_message_to_agent(self, to_agent: str, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """向另一个代理发送A2A消息"""
        if not self.registered:
            logger.error(f"Agent {self.agent_id} not registered, cannot send message")
            return None
        return self.nautilus.send_a2a_message(self.agent_id, to_agent, message)
    
    def receive_message(self, from_agent: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """处理接收到的消息（可被子类重写）"""
        logger.info(f"Agent {self.agent_id} received message from {from_agent}: {message}")
        # 默认返回确认
        return {"status": "received", "from": from_agent, "message_id": message.get("id")}
    
    def transfer_tokens(self, to_agent: str, amount: float) -> bool:
        """向另一个代理转移NAU代币"""
        if not self.registered:
            logger.error(f"Agent {self.agent_id} not registered, cannot transfer tokens")
            return False
        return self.nautilus.transfer_tokens(self.agent_id, to_agent, amount)
    
    def get_balance(self) -> Optional[float]:
        """查询当前代理的NAU余额"""
        if not self.registered:
            logger.error(f"Agent {self.agent_id} not registered, cannot get balance")
            return None
        return self.nautilus.get_balance(self.agent_id)
    
    def run(self, task: str, **kwargs) -> Any:
        """执行任务（promptulate Agent的核心方法）"""
        # 这里可以集成promptulate的推理逻辑
        logger.info(f"Agent {self.agent_id} executing task: {task}")
        # 示例：简单返回任务字符串
        return f"Agent {self.agent_id} completed task: {task}"

class NautilusTool(Tool):
    """封装Nautilus平台功能的工具，供promptulate代理使用"""
    
    def __init__(self, name: str, description: str, nautilus_client: NautilusClient):
        super().__init__(name=name, description=description)
        self.nautilus = nautilus_client
    
    def _run(self, **kwargs) -> Any:
        # 子类实现具体功能
        raise NotImplementedError

class A2ASendMessageTool(NautilusTool):
    """发送A2A消息的工具"""
    
    def __init__(self, nautilus_client: NautilusClient):
        super().__init__(
            name="a2a_send_message",
            description="通过A2A网关向另一个代理发送消息",
            nautilus_client=nautilus_client
        )
    
    def _run(self, from_agent: str, to_agent: str, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.nautilus.send_a2a_message(from_agent, to_agent, message)

class TokenTransferTool(NautilusTool):
    """转移NAU代币的工具"""
    
    def __init__(self, nautilus_client: NautilusClient):
        super().__init__(
            name="token_transfer",
            description="在代理之间转移NAU代币",
            nautilus_client=nautilus_client
        )
    
    def _run(self, from_agent: str, to_agent: str, amount: float) -> bool:
        return self.nautilus.transfer_tokens(from_agent, to_agent, amount)