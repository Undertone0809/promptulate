from promptulate.tools.base import Tool


class HuggingFaceTool(Tool):
    """Simple wrapper for huggingface transformers tools"""

    def __init__(self, tool, name: str, description: str, **kwargs):
        from transformers.tools import Tool as _HuggingFaceTool

        self.tool = tool
        self.name = name
        self.description = description

        if isinstance(tool, _HuggingFaceTool):
            raise ValueError("HuggingFaceTool should be type of transformers.tools")

        super().__init__(**kwargs)

    def _run(self, *args, **kwargs):
        return self.tool(*args, **kwargs)
