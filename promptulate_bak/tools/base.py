import inspect
import warnings
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Type, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Extra,
    create_model,
    validate_arguments,
    validate_call,
)

from promptulate.hook.base import Hook, HookTable
from promptulate.utils.logger import logger

if TYPE_CHECKING:
    from langchain.tools.base import BaseTool as LangchainBaseToolType  # noqa

ToolTypes = Union["BaseTool", "Tool", Callable, "LangchainBaseToolType", "BaseToolKit"]


_schema_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


def _create_subset_model(
    name: str, model: BaseModel, field_names: list
) -> type[BaseModel]:
    """Create a pydantic model with only a subset of model's fields."""
    fields = {}
    for field_name in field_names:
        field = model.model_fields[field_name]  # Updated to use model_fields
        fields[field_name] = (field.annotation, field)  # Updated to use annotation
    return create_model(name, **fields)


def _pydantic_to_refined_schema(pydantic_obj: type[BaseModel]) -> Dict[str, Any]:
    """Get refined schema(OpenAI function call type schema) from pydantic object."""
    # Remove useless fields.
    refined_schema = pydantic_obj.model_json_schema()

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
    # inferred_model = validate_call(func, config=_schema_config).model

    # Extract function parameter names.
    # Pydantic adds placeholder virtual fields we need to strip
    signature = inspect.signature(func)
    valid_properties: List[str] = [
        param.name for param in signature.parameters.values()
    ]

    created_model: type[BaseModel] = create_model(
        f"{func.__name__}Schema",
        **{
            param.name: (param.annotation, param)
            for param in signature.parameters.values()
        },
    )
    print(created_model.model_json_schema())

    # Create a pydantic model with only the valid fields.
    # created_model = _create_subset_model(
    #     f"{func.__name__}Schema", inferred_model, valid_properties
    # )
    reduced_schema = created_model.model_json_schema()

    # reduce schema
    reduced_schema["description"] = func.__doc__ or ""
    reduced_schema["name"] = func.__name__

    if "title" in reduced_schema:
        del reduced_schema["title"]

    for k, v in reduced_schema["properties"].items():
        if "title" in v:
            del v["title"]

    print(reduced_schema)

    return reduced_schema


class BaseTool(ABC, BaseModel):
    """Interface tools must implement."""

    name: str
    """The unique name of the tool that clearly communicates its purpose."""
    description: str
    """Used to tell the model how/when/why to use the tool.
    You can provide few-shot examples as a part of the description."""
    parameters: Optional[Union[Dict, type(BaseModel)]] = None
    """The parameters that the tool accepts. This can be a dictionary or a Pydantic
    model."""
    example: List[str] = None
    """Show how to use this tool. This is few shot for agent. You few shot may like:

    example1 = "Question: What is 37593 * 67?\n```\n37593 * 67\n```\nnumexpr.evaluate("37593 * 67")\nAnswer:2518731"
    example2 = "Question: What is 37593^(1/5)?\n```\n37593**(1/5)\n```\nnumexpr.evaluate("37593**(1/5)")\nAnswer:8.222831614237718"
    few_shot_example = [example1, example2]
    """  # noqa

    def __init__(self, **kwargs):
        """Custom tool config.

        Args:
            **kwargs:
                hooks(List[Callable]): for adding to hook_manager
        """
        warnings.warn(
            "BaseTool is deprecated at v1.7.0. promptulate.tools.base.Tool and function type declaration is recommended.",  # noqa: E501
            DeprecationWarning,
        )
        super().__init__(**kwargs)
        if "hooks" in kwargs and kwargs["hooks"]:
            for hook in kwargs["hooks"]:
                Hook.mount_instance_hook(hook, self)
        Hook.call_hook(HookTable.ON_TOOL_CREATE, self, **kwargs)

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")

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
    """Abstract base class for tools. All tools must implement this interface.

    Attributes:
        name(str): Tool name
        description(str): Tool description
        parameters(Optional[Union[Dict, type(BaseModel)]]): Tool parameters, default is
            None.
    """

    name: str
    description: str
    parameters: Optional[Union[Dict, type(BaseModel)]] = None

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

    def _args_to_kwargs(self, *args, **kwargs) -> Dict:
        """Converts positional arguments to keyword arguments based on tool parameters.

        This method takes in both positional and keyword arguments. It then attempts to
        match the positional arguments to the tool's parameters, converting them to
        keyword arguments. Any additional keyword arguments are also included in the
        final dictionary.

        Returns:
            Dict: A dictionary containing the converted keyword arguments.
        """
        all_kwargs = {}

        if isinstance(self.parameters, dict) and "properties" in self.parameters:
            all_kwargs.update(dict(zip(self.parameters["properties"].keys(), args)))
        elif isinstance(self.parameters, type) and issubclass(
            self.parameters, BaseModel
        ):
            all_kwargs.update(dict(zip(self.parameters.__fields__.keys(), args)))

        all_kwargs.update(kwargs)

        return all_kwargs


class ToolImpl(Tool):
    def __init__(
        self,
        name: str,
        description: str,
        callback: Callable,
        parameters: Union[dict, BaseModel] = None,
        **kwargs,
    ):
        self.name: str = name
        self.description: str = description
        self.callback: Callable = callback
        self.parameters: Union[dict, BaseModel] = parameters

        super().__init__(**kwargs)

    @classmethod
    def from_function(cls, func: Callable) -> "ToolImpl":
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
        parameters: Optional[Union[Dict, type(BaseModel)]] = None,
    ) -> "ToolImpl":
        """Create a ToolImpl instance from a function.

        Args:
            callback: Function to create the ToolImpl instance from.
            name: tool name
            description: tool description
            parameters: tool parameters

        Returns:
            A ToolImpl instance.
        """
        _name = name or callback.__name__
        _description = description or callback.__doc__ or ""

        if parameters:
            if isinstance(parameters, dict):
                schema = parameters
            elif isinstance(parameters, type) and issubclass(parameters, BaseModel):
                schema = _pydantic_to_refined_schema(parameters)
            else:
                raise TypeError(
                    f"{[cls.__name__]} parameters must be BaseModel or JSON schema."
                )  # noqa
        else:
            schema = function_to_tool_schema(callback)
            schema["name"] = _name
            schema["description"] = _description

        return cls(
            name=schema["name"],
            description=schema["description"],
            callback=callback,
            parameters=schema,
        )

    @classmethod
    def from_base_tool(cls, tool: BaseTool) -> "ToolImpl":
        """Create a ToolImpl instance from a BaseTool instance.

        Args:
            tool: BaseTool instance to create the ToolImpl instance from.

        Returns:
            A ToolImpl instance.
        """

        return cls(
            name=tool.name,
            description=tool.description,
            callback=tool.run,
            parameters=tool.parameters,
        )

    def _run(self, *args, **kwargs):
        return self.callback(*args, **kwargs)


def define_tool(
    *,
    callback: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters: Union[dict, type(BaseModel)] = None,
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
    """Base class for toolkits. This class can be inherited when you want to initialize
    multiple tools simultaneously. The initialization method of this class is suitable
    for tools that require state management, such as file read and write operations,
    which need to declare their workspace during initialization.
    """

    @abstractmethod
    def get_tools(self) -> List[ToolTypes]:
        """get tools in the toolkit"""
        raise NotImplementedError
