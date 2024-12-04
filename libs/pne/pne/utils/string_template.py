import re
from typing import Any, List

from typing_extensions import Literal


def _get_jinja2_variables(template: str) -> List[str]:
    try:
        from jinja2 import Environment, meta
    except ImportError:
        raise ImportError(
            "jinja2 not installed, which is needed to use the jinja2_formatter. "
            "Please install it with `pip install jinja2`."
        )
    env = Environment()
    ast = env.parse(template)
    variables = meta.find_undeclared_variables(ast)
    return list(variables)


def _jinja2_format(template: str, **kwargs) -> str:
    """Format a template using jinja2.

    *Security warning*: As of LangChain 0.0.329, this method uses Jinja2's
        SandboxedEnvironment by default. However, this sand-boxing should
        be treated as a best-effort approach rather than a guarantee of security.
        Do not accept jinja2 templates from untrusted sources as they may lead
        to arbitrary Python code execution.

        https://jinja.palletsprojects.com/en/3.1.x/sandbox/
    """
    try:
        from jinja2.sandbox import SandboxedEnvironment
    except ImportError:
        raise ImportError(
            "jinja2 not installed, which is needed to use the jinja2_formatter. "
            "Please install it with `pip install jinja2`."
            "Please be cautious when using jinja2 templates. "
            "Do not expand jinja2 templates using unverified or user-controlled "
            "inputs as that can result in arbitrary Python code execution."
        )

    # This uses a sandboxed environment to prevent arbitrary code execution.
    # Jinja2 uses an opt-out rather than opt-in approach for sand-boxing.
    # Please treat this sand-boxing as a best-effort approach rather than
    # a guarantee of security.
    # We recommend to never use jinja2 templates with untrusted inputs.
    # https://jinja.palletsprojects.com/en/3.1.x/sandbox/
    # approach not a guarantee of security.
    return SandboxedEnvironment().from_string(template).render(**kwargs)


class StringTemplate:
    """String Template for llm. It can generate a complex prompt."""

    def __init__(
        self, template: str, template_format: Literal["f-string", "jinja2"] = "f-string"
    ):
        self.template: str = template
        self.template_format: str = template_format
        self.variables: List[str] = []

        if template_format == "f-string":
            self.variables = re.findall(r"\{(\w+)\}", self.template)
        elif template_format == "jinja2":
            self.variables = _get_jinja2_variables(template)
        else:
            raise ValueError(
                f"template_format must be one of 'f-string' or 'jinja2'. Got: {template_format}"  # noqa: E501
            )

    def format(self, params: List[Any] = None, **kwargs) -> str:
        """Enter variables and return the formatted string."""
        if params:
            kwargs = {}
            for i, param in enumerate(params):
                kwargs.update({self.variables[i]: param})

        if self.template_format == "f-string":
            return self.template.format(**kwargs)
        elif self.template_format == "jinja2":
            return _jinja2_format(self.template, **kwargs)
