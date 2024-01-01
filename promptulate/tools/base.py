import inspect
import warnings
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type, Union

from promptulate.hook.base import Hook, HookTable
from promptulate.pydantic_v1 import BaseModel, Extra, create_model, validate_arguments
from promptulate.utils.logger import logger


class _SchemaConfig:
    """Configuration for the pydantic model."""

    extra: Any = Extra.forbid
    arbitrary_types_allowed: bool = True


def _create_subset_model(
    name: str, model: BaseModel, field_names: list
) -> Type[BaseModel]:
    """Create a pydantic model with only a subset of model's fields."""
    fields = {}
    for field_name in field_names:
        field = model.__fields__[field_name]
        fields[field_name] = (field.outer_type_, field.field_info)
    return create_model(name, **fields)


def _pydantic_to_refined_schema(pydantic_obj: type(BaseModel)) -> Dict[str, Any]:
    """Get refined schema(OpenAI function call type schema) from pydantic object."""
    # Remove useless fields.
    refined_schema = pydantic_obj.schema()

    if "title" in refined_schema:
        del refined_schema["title"]
    for k, v in refined_schema["properties"].items():
        if "title" in v:
            del v["title"]

    return refined_schema


def _validate_refined_schema(schema: Dict) -> bool:
    """Validate refined schema(OpenAI function call type schema).

    Args:
        schema: any dict

    Returns:
        bool: True if schema is openai function call type schema, False otherwise.
    """
    if "name" not in schema or "description" not in schema:
        return False

    if "properties" not in schema:
        return False

    return True


def function_to_tool_schema(func: Callable) -> Dict[str, Any]:
    """Create a tool schema from a function's signature.

    Args:
        func: Function to generate the schema from

    Returns:
        A OpenAI function call type json schema built by pydantic model.
        ref: https://platform.openai.com/docs/api-reference/chat/create#chat-create-function_call
    """  # noqa
    # https://docs.pydantic.dev/latest/usage/validation_decorator/
    inferred_model = validate_arguments(func, config=_SchemaConfig).model  # type: ignore # noqa

    # Extract function parameter names.
    # Pydantic adds placeholder virtual fields we need to strip
    signature = inspect.signature(func)
    valid_properties: List[str] = [
        param.name for param in signature.parameters.values()
    ]

    # Create a pydantic model with only the valid fields.
    created_model = _create_subset_model(
        f"{func.__name__}Schema", inferred_model, valid_properties
    )
    reduced_schema = created_model.schema()

    # reduce schema
    reduced_schema["description"] = func.__doc__ or ""
    reduced_schema["name"] = func.__name__

    if "title" in reduced_schema:
        del reduced_schema["title"]
    for k, v in reduced_schema["properties"].items():
        if "title" in v:
            del v["title"]

    return reduced_schema


class BaseTool(ABC, BaseModel):
    """Interface tools must implement."""

    name: str
    """The unique name of the tool that clearly communicates its purpose."""
    description: str
    """Used to tell the model how/when/why to use the tool.
    You can provide few-shot examples as a part of the description."""
    example: List[str] = None
    """Show how to use this tool. This is few shot for agent. You few shot may like:

    example1 = "Question: What is 37593 * 67?\n```\n37593 * 67\n```\nnumexpr.evaluate("37593 * 67")\nAnswer:2518731"
    example2 = "Question: What is 37593^(1/5)?\n```\n37593**(1/5)\n```\nnumexpr.evaluate("37593**(1/5)")\nAnswer:8.222831614237718"
    few_shot_example = [example1, example2]
    """  # noqa

    # hook_manager: Optional[HookManager] = Field(default=HookManager())
    # """Hook manager will call hook function at the specified lifecycle."""

    def __init__(self, **kwargs):
        """Custom tool config.

        Args:
            **kwargs:
                hooks(List[Callable]): for adding to hook_manager
        """
        warnings.warn(
            "BaseTool is deprecated at v1.7.0. promptulate.tools.base.Tool is recommended.",  # noqa: E501
            DeprecationWarning,
        )
        super().__init__(**kwargs)
        if "hooks" in kwargs and kwargs["hooks"]:
            for hook in kwargs["hooks"]:
                Hook.mount_instance_hook(hook, self)
        Hook.call_hook(HookTable.ON_TOOL_CREATE, self, **kwargs)

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow

    def run(self, *args, **kwargs):
        """run the tool including specified function and hooks"""
        Hook.call_hook(HookTable.ON_TOOL_START, self, *args, **kwargs)
        result: Any = self._run(*args, **kwargs)
        logger.debug(f"[pne tool result] {result}")
        Hook.call_hook(HookTable.ON_TOOL_RESULT, self, result=result)
        return result

    @abstractmethod
    def _run(self, *args, **kwargs):
        """Run detail business, implemented by subclass."""
        raise NotImplementedError()


class Tool(ABC):
    """Abstract base class for tools. All tools must implement this interface."""

    name: str
    """Tool name"""
    description: str
    """Tool description"""
    parameters: Optional[Union[Dict, Type[BaseModel]]] = None
    """Tool parameters"""

    def __init__(self, *args, **kwargs):
        self.check_params()
        if "hooks" in kwargs and kwargs["hooks"]:
            for hook in kwargs["hooks"]:
                Hook.mount_instance_hook(hook, self)
        Hook.call_hook(HookTable.ON_TOOL_CREATE, self, **kwargs)

    def check_params(self):
        """Check parameters when initialization."""
        if not getattr(self, "name", None) or not getattr(self, "description", None):
            raise TypeError(
                f"{self.__class__.__name__} required parameters 'name' and 'description'."  # noqa: E501
            )

    def run(self, *args, **kwargs):
        """run the tool including specified function and hooks"""
        Hook.call_hook(HookTable.ON_TOOL_START, self, *args, **kwargs)
        result: Any = self._run(*args, **kwargs)
        logger.debug(f"[pne tool response] name: {self.name} result: {result}")
        Hook.call_hook(HookTable.ON_TOOL_RESULT, self, result=result)
        return result

    @abstractmethod
    def _run(self, *args, **kwargs):
        """Run detail business, implemented by subclass."""
        raise NotImplementedError()

    def to_schema(self) -> Dict[str, Any]:
        """
        Converts the Tool instance to a OpenAI function call type JSON schema.

        Returns:
            dict: A dictionary representing the JSON schema of the Tool instance.
        """
        # If there are no parameters, return the basic schema.
        if not self.parameters:
            return {
                "name": self.name,
                "description": self.description,
            }

        # If parameters are defined by a Pydantic BaseModel, convert to schema.
        if isinstance(self.parameters, type) and issubclass(self.parameters, BaseModel):
            return {
                "name": self.name,
                "description": self.description,
                "parameters": _pydantic_to_refined_schema(self.parameters),
            }

        # If parameters are defined by a schema dictionary, validate and return it.
        if isinstance(self.parameters, dict):
            if not _validate_refined_schema(self.parameters):
                raise ValueError(
                    f"The 'parameters' dictionary for {self.__class__.__name__} does not conform to the expected schema."  # noqa: E501
                )
            return self.parameters

        # If parameters are neither a BaseModel nor a dictionary, raise an error.
        raise TypeError(
            f"The 'parameters' attribute of {self.__class__.__name__} must be either a subclass of BaseModel or a dictionary representing a schema."  # noqa: E501
        )


class ToolImpl(Tool):
    def __init__(
        self,
        name: str,
        description: str,
        callback: Callable,
        parameters: Union[dict, BaseModel] = None,
        **kwargs,
    ):
        self.name: str = name or ""
        self.description: str = description or ""
        self.parameters: Union[dict, BaseModel] = parameters
        self.callback: Callable = callback

        super().__init__(**kwargs)

    @classmethod
    def from_function(cls, func: Callable):
        """Create a ToolImpl instance from a function.

        Args:
            func: Function to create the ToolImpl instance from.

        Returns:
            A ToolImpl instance.
        """
        if not func.__doc__:
            err_msg = """Please add docstring and variable type declarations for your function.Here is a best practice:
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

        schema = function_to_tool_schema(func)
        return cls(
            name=func.__name__,
            description=func.__doc__,
            callback=func,
            parameters=schema,
        )

    @classmethod
    def from_define_tool(
        cls,
        callback: Callable,
        name: str = None,
        description: str = None,
        parameters: Union[dict, BaseModel] = None,
    ):
        """Create a ToolImpl instance from a function.

        Args:
            callback: Function to create the ToolImpl instance from.
            name: tool name
            description: tool description
            parameters: tool parameters

        Returns:
            A ToolImpl instance.
        """
        if not parameters:
            schema: dict = function_to_tool_schema(callback)
        elif isinstance(parameters, dict) and _validate_refined_schema(parameters):
            schema: dict = parameters
        elif isinstance(parameters, type) and issubclass(parameters, BaseModel):
            schema: dict = _pydantic_to_refined_schema(parameters)
        else:
            raise TypeError(
                f"{[cls.__name__]} parameters must be BaseModel or JSON schema."
            )

        _description = description or ""
        _doc = callback.__doc__ or ""

        return cls(
            name=name or callback.__name__,
            description=f"{_description}\n{_doc}",
            callback=callback,
            parameters=schema,
        )

    def _run(self, *args, **kwargs):
        return self.callback(*args, **kwargs)


def define_tool(
    *,
    callback: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters: Union[dict, BaseModel] = None,
) -> ToolImpl:
    """
    A tool with llm or API wrapper will automatically initialize the llm and API wrapper
    classes, which can avoid this problem by initializing in this way.

    Args:
        callback: tool function when running
        name: tool name
        description: tool description
        parameters: tool parameters

    Returns:
        A ToolImpl class (subclass of Tool).
    """

    return ToolImpl.from_define_tool(
        callback=callback, name=name, description=description, parameters=parameters
    )


def function_to_tool(func: Callable) -> ToolImpl:
    """Converts a function to a ToolImpl instance.

    Args:
        func: Function to convert to a ToolImpl instance.

    Returns:
        A ToolImpl instance.
    """
    return ToolImpl.from_function(func)


class BaseToolKit:
    @abstractmethod
    def get_tools(self):
        """get tools in the toolkit"""
