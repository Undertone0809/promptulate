def get_llm_cls(platform_type, model_name, model_config):
    if platform_type == "qianfan":
        from promptulate.llms import QianFan

        if model_name == "":
            return QianFan(model_config=model_config)
        else:
            return QianFan(model=model_name, model_config=model_config)
    elif platform_type == "zhipu":
        from promptulate.llms import ZhiPu

        if model_name == "":
            return ZhiPu(model_config=model_config)
        else:
            return ZhiPu(model=model_name, model_config=model_config)
    elif platform_type == "custom_llm":
        from promptulate.llms import CustomLLM

        if model_name == "":
            return CustomLLM(model_config=model_config)
        else:
            return CustomLLM(model=model_name, model_config=model_config)
    else:
        raise ImportError("not found this platform")


class LLMFactory:
    @classmethod
    def build(
        self, platform_type: str, model_name: str = None, model_config: {} = None
    ):
        if model_config is None:
            model_config = {}
        model_name: str = model_name or ""
        return get_llm_cls(
            platform_type=platform_type,
            model_name=model_name,
            model_config=model_config,
        )
