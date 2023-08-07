import re
from typing import List, Any


class StringTemplate:
    """String Template for llm. It can generate a complex prompt."""

    template: str
    variables: List[str]

    def __init__(self, template: str):
        self.template = template
        self._fetch_variables()

    def _fetch_variables(self):
        self.variables = re.findall(r"\{(\w+)\}", self.template)

    def format(self, params: List[Any] = None, **kwargs) -> str:
        """Enter variables and return the formatted string."""
        if params:
            kwargs = {}
            for i, param in enumerate(params):
                kwargs.update({self.variables[i]: param})

        return self.template.format(**kwargs)
