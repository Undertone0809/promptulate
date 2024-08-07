from typing import Any, Dict, Optional

from promptulate.llms._litellm import LiteLLM
from promptulate.llms.base import BaseLLM


class LLMFactory:
    @classmethod
    def build(
        cls, model_name: str, *, model_config: Optional[Dict[str, Any]] = None, max_retry: int = 5, **kwargs
    ) -> BaseLLM:
        model_config = model_config or {}

        try:
            provider, model_id = model_name.split("/")

            if provider == "zhipu":
                from promptulate.llms import ZhiPu

                return ZhiPu(model=model_id, model_config=model_config, max_retry=max_retry, **kwargs)
            elif provider == "qianfan":
                from promptulate.llms import QianFan

                return QianFan(model=model_id, model_config=model_config, max_retry=max_retry, **kwargs)
        except ValueError:
            pass

        return LiteLLM(model=model_name, model_config=model_config, max_retry=max_retry, **kwargs)
