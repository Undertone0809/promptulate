import json
import logging
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)

class NautilusClient:
    """Nautilus平台客户端，封装与平台交互的API"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    def register_agent(self, agent_id: str, capabilities: list, metadata: Dict[str, Any]) -> bool:
        """在Nautilus平台注册代理"""
        url = f"{self.base_url}/api/v1/agents/register"
        payload = {
            'agent_id': agent_id,
            'capabilities': capabilities,
            'metadata': metadata
        }
        try:
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Agent {agent_id} registered successfully")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            return False
    
    def send_a2a_message(self, from_agent: str, to_agent: str, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """通过A2A网关发送消息"""
        url = f"{self.base_url}/api/v1/a2a/send"
        payload = {
            'from': from_agent,
            'to': to_agent,
            'message': message
        }
        try:
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send A2A message from {from_agent} to {to_agent}: {e}")
            return None
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取代理信息"""
        url = f"{self.base_url}/api/v1/agents/{agent_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get agent info for {agent_id}: {e}")
            return None
    
    def transfer_tokens(self, from_agent: str, to_agent: str, amount: float, token: str = "NAU") -> bool:
        """在代理之间转移NAU代币"""
        url = f"{self.base_url}/api/v1/tokens/transfer"
        payload = {
            'from': from_agent,
            'to': to_agent,
            'amount': amount,
            'token': token
        }
        try:
            response = self.session.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Transferred {amount} {token} from {from_agent} to {to_agent}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to transfer tokens: {e}")
            return False
    
    def get_balance(self, agent_id: str, token: str = "NAU") -> Optional[float]:
        """查询代理的代币余额"""
        url = f"{self.base_url}/api/v1/tokens/balance/{agent_id}"
        params = {'token': token}
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('balance')
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get balance for {agent_id}: {e}")
            return None
    
    def close(self):
        """关闭会话"""
        self.session.close()