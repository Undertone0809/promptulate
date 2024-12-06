import inspect
import json
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Union

from docstring_parser import parse
from pydantic import BaseModel

# TODO: add langchain tool support
ToolTypes = Union[Callable, "Tool", "ToolKit"]


class ToolParameters(BaseModel):
    """Defines the schema of a tool's parameters."""

    type: str = "object"
    properties: Dict[str, Any]
    required: List[str] = []
    additionalProperties: bool = False


class Tool(BaseModel):
    """Represents a functional tool with metadata for usage in an automated system."""

    name: str
    description: str
    parameters: ToolParameters
    function: Callable

    def run(self, *args, **kwargs) -> str:
        """Run the tool."""
        return self.function(*args, **kwargs)

    def to_function_schema(self) -> Dict[str, Any]:
        """Convert the tool to OpenAI function call type JSON schema.

        Example:
            >>> def add(a: int, b: int) -> int:
            ...     \"""Adds two integers.
            ...
            ...     Args:
            ...         a: First integer.
            ...         b: Second integer.
            ...
            ...     Returns:
            ...         Sum of a and b.
            ...     \"""
            ...     return a + b
            >>> tool = Tool.from_function(add)
            >>> tool.to_function_schema()
            {
                'name': 'add',
                'description': 'Adds two integers.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'a': {'type': 'integer', 'description': 'First integer.'},
                        'b': {'type': 'integer', 'description': 'Second integer.'}
                    },
                    'required': ['a', 'b']
                }
            }
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters.model_dump(),
        }

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to OpenAI function schema format.

        Example:
            >>> def add(a: int, b: int) -> int:
            ...     \"""Adds two integers.
            ...
            ...     Args:
            ...         a: First integer.
            ...         b: Second integer.
            ...
            ...     Returns:
            ...         Sum of a and b.
            ...     \"""
            ...     return a + b
            >>> tool = Tool.from_function(add)
            >>> tool.to_tool_schema()
            {
                'type': 'function',
                'function': {
                    'name': 'add',
                    'description': 'Adds two integers.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'a': {'type': 'integer', 'description': 'First integer.'},
                            'b': {'type': 'integer', 'description': 'Second integer.'}
                        },
                        'required': ['a', 'b']
                    }
                }
            }
        """
        return {
            "type": "function",
            "function": self.to_function_schema(),
        }

    @classmethod
    def from_function(cls, func: Callable) -> "Tool":
        """
        Create a Tool instance from a callable.

        Args:
            func: Callable to create the Tool instance from.

        Returns:
            A Tool instance.

        Example:
            >>> def add(a: int, b: int) -> int:
            ...     \"""Adds two integers.
            ...
            ...     Args:
            ...         a: First integer.
            ...         b: Second integer.
            ...
            ...     Returns:
            ...         Sum of a and b.
            ...     \"""
            ...     return a + b
            >>> tool = Tool.from_function(add)
            >>> tool.name
            'add'
            >>> tool.description
            'Adds two integers.'
            >>> tool.parameters
            {'a': {'type': 'integer', 'description': 'First integer.'}, 'b': {'type':
            'integer', 'description': 'Second integer.'}}

        Raises:
            ValueError: If the callable lacks a docstring or parameter type hints.
        """
        if not func.__doc__:
            raise ValueError(
                "Function must have a docstring describing its parameters and return values."  # noqa
            )

        # Extract metadata
        name = func.__name__
        description = cls._parse_description(func.__doc__)
        sig = inspect.signature(func)
        parameters = cls._parse_parameters(sig, func)

        return cls(
            name=name,
            description=description,
            parameters=ToolParameters(
                type="object",
                properties=parameters,
                required=[
                    param_name
                    for param_name, param in sig.parameters.items()
                    if param.default == inspect.Parameter.empty
                ],
                additionalProperties=False,
            ),
            function=func,
        )

    @staticmethod
    def _parse_description(docstring: str) -> str:
        """Parse and clean the function's docstring.

        Args:
            docstring: Function docstring.
        """
        parsed_doc = parse(docstring)
        return parsed_doc.short_description or docstring.strip()

    @classmethod
    def _parse_parameters(
        cls, sig: inspect.Signature, func: Callable
    ) -> Dict[str, Dict[str, Any]]:
        """
        Parse and convert function parameters to JSON schema.

        Args:
            sig: Function signature object.
            func: Original callable.

        Returns:
            Dictionary of parameters in JSON schema format.
        """
        parameters = {}
        for param_name, param in sig.parameters.items():
            if param_name == "self":  # Skip self for instance methods
                continue

            if param.annotation == inspect.Parameter.empty:
                raise ValueError(
                    f"Parameter {param_name} in function '{func.__name__}' must have type hints. "  # noqa
                    "Supported types: str, int, float, bool, list, dict."
                )

            parameters[param_name] = {
                "type": cls._python_type_to_json_type(param.annotation),
                "description": f"Parameter {param_name}",
            }
        return parameters

    @staticmethod
    def _python_type_to_json_type(py_type: Any) -> str:
        """
        Convert Python types to JSON schema types.

        Args:
            py_type: Python type.

        Returns:
            JSON schema type.

        Raises:
            TypeError: If the type is not supported.
        """
        type_mapping = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object",
        }
        if py_type not in type_mapping:
            raise TypeError(
                f"Unsupported type: {py_type}. Supported types are: {list(type_mapping.keys())}"  # noqa: E501
            )
        return type_mapping[py_type]


class ToolKit(ABC):
    """Abstract base class for a collection of tools."""

    def __init__(self):
        self.tools: Dict[str, Tool] = OrderedDict()

    def register(self, func: Callable) -> None:
        """
        Register a callable as a Tool in the toolkit.

        Args:
            func: Callable to register.
        """
        tool = Tool.from_function(func)
        self.tools[tool.name] = tool
