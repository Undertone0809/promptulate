import inspect
import json
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Literal, TypeVar, Union

from docstring_parser import parse
from pydantic import BaseModel

ToolTypes = Union[Callable, "Tool", "ToolKit"]


class ToolParameters(BaseModel):
    type: str = "object"
    properties: Dict[str, Any]
    required: List[str] = []
    additionalProperties: bool = False


class Tool(BaseModel):
    name: str
    description: str
    parameters: ToolParameters

    def to_function_call(self) -> Dict[str, Any]:
        """Convert the tool to OpenAI function call type JSON schema."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters.model_dump(),
        }

    def to_tool_call_schema(self) -> Dict[str, Any]:
        """Convert the tool to OpenAI function schema format."""
        return {
            "type": "function",
            "function": self.to_function_call(),
        }

    @classmethod
    def from_function(cls, func: Callable) -> "Tool":
        """Create a Tool instance from a function.

        Args:
            func: Function to create the Tool instance from.

        Returns:
            A Tool instance.
        """
        if not func.__doc__:
            err_msg = """Please add docstring and variable type declarations for your function. Here is a best practice:
def web_search(keyword: str, top_k: int = 10) -> str:
    \"""search by keyword in web.
    Args:
        keyword: keyword to search
        top_k: top k results to return

    Returns:
        str: search result
    \"""
    return "result"
            """  # noqa
            raise ValueError(err_msg)

        name = func.__name__
        description = func.__doc__

        # Parse docstring
        parsed_doc = parse(description)
        parameter_docs = {p.arg_name: p.description for p in parsed_doc.params}

        sig = inspect.signature(func)

        parameters = {}
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue

            param_type = param.annotation
            if param_type == inspect.Parameter.empty:
                raise ValueError(
                    f"Parameter {param_name} in {func.__name__} must have type hints"
                    "Suppoerted type: str, int, float, bool, list, dict"
                )

            json_type = cls._python_type_to_json_type(param_type)
            param_description = parameter_docs.get(
                param_name, f"Parameter {param_name}"
            )

            parameters[param_name] = {
                "type": json_type,
                "description": param_description,
            }

        # Finalize description based on parsed docstring
        if not parameter_docs:  # If no specific style detected, use full docstring
            description = description.strip()

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
        )

    @staticmethod
    def _python_type_to_json_type(py_type):
        """Convert Python types to JSON schema types."""
        if py_type in {str, int, float, bool, list, dict}:
            return {
                str: "string",
                int: "integer",
                float: "number",
                bool: "boolean",
                list: "array",
                dict: "object",
            }[py_type]
        raise TypeError(f"Unsupported type: {py_type}")


# class Tool(ABC):
#     name: str
#     description: str
#     parameters: Dict[str, Any]
#     function: Callable

#     def __init__(
#         self,
#         name: str,
#         description: str,
#         parameters: Dict[str, Any],
#         function: Callable,
#     ):
#         self.name = name
#         self.description = description
#         self.parameters = parameters
#         self.function = function

#     def run(self, *args, **kwargs) -> str:
#         """Execute the tool function with given arguments."""
#         return self.function(*args, **kwargs)

#     def to_tool_call_schema(self) -> Dict[str, Any]:
#         """Convert the tool to OpenAI function schema format."""
#         return {
#             "type": "function",
#             "function": {
#                 "name": self.name,
#                 "description": self.description,
#                 "parameters": {
#                     "type": "object",
#                     "properties": self.parameters,
#                     "required": list(self.parameters.keys()),
#                     "additionalProperties": False,
#                 },
#             },
#         }

#     @classmethod
#     def from_function(cls, func: Callable) -> "Tool":
#         """Create a Tool instance from a function.

#         Args:
#             func (Callable): The function to convert into a tool.

#         Returns:
#             Tool: A new Tool instance.

#         Raises:
#             ValueError: If the function lacks proper docstring or type hints.
#         """
#         # Get function signature
#         sig = inspect.signature(func)

#         # Get docstring and validate
#         doc = inspect.getdoc(func)
#         if not doc:
#             raise ValueError(f"Function {func.__name__} must have a docstring")

#         # Build parameters schema
#         parameters = {}
#         for name, param in sig.parameters.items():
#             # Skip 'self' parameter for methods
#             if name == "self":
#                 continue

#             param_type = param.annotation
#             if param_type == inspect.Parameter.empty:
#                 raise ValueError(
#                     f"Parameter {name} in {func.__name__} must have type hints"
#                 )

#             parameters[name] = {
#                 "type": cls._python_type_to_json_type(param_type),
#                 "description": f"Parameter {name}",
#             }

#         return cls(
#             name=func.__name__,
#             description=doc.split("\n")[0],  # Just use the first line as description
#             parameters=parameters,
#             function=func,
#         )

#     @staticmethod
#     def _python_type_to_json_type(py_type: type) -> str:
#         """Convert Python type to JSON schema type."""
#         type_map = {
#             str: "string",
#             int: "integer",
#             float: "number",
#             bool: "boolean",
#             list: "array",
#             dict: "object",
#         }
#         return type_map.get(py_type, "string")


class ToolKit(ABC):
    def __init__(self):
        self.tools: Dict[str, Tool] = OrderedDict()

    def register(self, func: Callable) -> None:
        tool = Tool.from_function(func)
        self.tools[tool.name] = tool


class FileToolKit(ToolKit):
    def __init__(self, root_dir: str = "./"):
        super().__init__()

        self.root_dir = root_dir

        self.register(self.read_file)
        self.register(self.write_file)
        self.register(self.delete_file)
        self.register(self.list_files)

    def read_file(self, file_name: str) -> str: ...

    def write_file(self, file_name: str, content: str) -> str: ...

    def delete_file(self, file_name: str) -> str: ...

    def list_files(self) -> List[str]: ...
