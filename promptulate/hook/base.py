import logging
from typing import Callable, List, Optional, Tuple, Union

from pydantic import BaseModel
from typing_extensions import Literal

from promptulate.utils.core_utils import generate_unique_id

logger = logging.getLogger(__name__)
HOOK_TYPE = Literal["component", "instance"]
# Hook component type
COMPONENT_TYPE = Literal["Tool", "llm", "Agent"]


class HookTable:
    ON_LLM_CREATE = ("llm", "on_llm_create")
    ON_LLM_START = ("llm", "on_llm_start")
    ON_LLM_RESULT = ("llm", "on_llm_result")

    ON_TOOL_CREATE = ("Tool", "on_tool_create")
    ON_TOOL_START = ("Tool", "on_tool_start")
    ON_TOOL_RESULT = ("Tool", "on_tool_result")

    ON_AGENT_CREATE = ("Agent", "on_agent_create")
    ON_AGENT_START = ("Agent", "on_agent_start")
    ON_AGENT_ACTION = ("Agent", "on_agent_action")
    ON_AGENT_OBSERVATION = ("Agent", "on_agent_observation")
    ON_AGENT_RESULT = ("Agent", "on_agent_result")


class BaseHookSchema(BaseModel):
    hook_name: str
    """Hook lifecycle."""
    callback: Callable
    """Callback function of hook."""
    component_type: COMPONENT_TYPE
    """Component type for hook."""

    def __str__(self):
        return f"<HookSchema> hook_name: {self.hook_name} callback: {self.callback} component_type: {self.component_type}"  # noqa


ComponentHookSchema = BaseHookSchema


class InstanceHookSchema(BaseHookSchema):
    mounted_obj: Optional[object]
    """Mounted obj call hooks. When hook is registered as None, it will only be assigned
    a value when the component is instantiated."""
    unique_id: str

    def __str__(self):
        return (
            f"<HookSchema> hook_name: {self.hook_name} callback: {self.callback} component_type: "  # noqa
            f"{self.component_type} mounted_obj: {self.mounted_obj.__class__.__name__}"
        )


def _hook_decorator(
    hook_table: Tuple,
    hook_type: HOOK_TYPE,
    fn: Callable,
):
    """Hook decorator wrapper for HookMixin"""
    unique_id = generate_unique_id()

    if hook_type == "instance":
        Hook.registry_instance_hook(hook_table, fn, unique_id)
    elif hook_type == "component":
        Hook.registry_component_hook(hook_table, fn)
    else:
        raise ValueError("hook type error, `instance` or `component` are specified.")

    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    wrapper.__unique_id__ = unique_id

    return wrapper


class ToolHookMixin:
    @staticmethod
    def on_tool_create(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_TOOL_CREATE, hook_type, fn)

        return decorator

    @staticmethod
    def on_tool_start(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_TOOL_START, hook_type, fn)

        return decorator

    @staticmethod
    def on_tool_result(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_TOOL_RESULT, hook_type, fn)

        return decorator


class AgentHookMixin:
    @staticmethod
    def on_agent_create(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_AGENT_CREATE, hook_type, fn)

        return decorator

    @staticmethod
    def on_agent_start(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_AGENT_START, hook_type, fn)

        return decorator

    @staticmethod
    def on_agent_action(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_AGENT_ACTION, hook_type, fn)

        return decorator

    @staticmethod
    def on_agent_observation(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_AGENT_OBSERVATION, hook_type, fn)

        return decorator

    @staticmethod
    def on_agent_result(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_AGENT_RESULT, hook_type, fn)

        return decorator


class LLMHookMixin:
    @staticmethod
    def on_llm_create(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_LLM_CREATE, hook_type, fn)

        return decorator

    @staticmethod
    def on_llm_start(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_LLM_START, hook_type, fn)

        return decorator

    @staticmethod
    def on_llm_result(hook_type: HOOK_TYPE):
        def decorator(fn):
            return _hook_decorator(HookTable.ON_LLM_RESULT, hook_type, fn)

        return decorator


class Hook(ToolHookMixin, AgentHookMixin, LLMHookMixin):
    component_hook_store: List[ComponentHookSchema] = []
    instance_hook_store: List[InstanceHookSchema] = []
    unmounted_hook_store: List[InstanceHookSchema] = []

    @classmethod
    def registry_hook(
        cls,
        hook_table: Tuple,
        callbacks: Union[Callable, List[Callable]],
        hook_type: HOOK_TYPE,
    ):
        """Registry component or instance hook to the hook center for unified
        management."""
        if isinstance(callbacks, Callable):
            callbacks = [callbacks]

        for callback in callbacks:
            if hook_type == "component":
                cls.registry_component_hook(hook_table, callback)
            elif hook_type == "instance":
                cls.registry_instance_hook(hook_table, callback)

    @classmethod
    def registry_component_hook(cls, hook_table: Tuple, callback: Callable):
        hook = ComponentHookSchema(
            hook_name=hook_table[1],
            callback=callback,
            component_type=hook_table[0],
        )
        logger.debug(f"[pne hook registry] instance hook: {hook}")
        cls.component_hook_store.append(hook)

    @classmethod
    def registry_instance_hook(
        cls,
        hook_table: Tuple,
        callback: Callable,
        unique_id: Optional[str] = None,
    ):
        """Registry instance hook firstly, it still needs to be mounted by
        `mount_instance_hook`

        Args:
            hook_table: hook table
            callback: hook callback
            unique_id: a temporary variable
        """
        if not unique_id and not getattr(callback, "__unique_id__", None):
            unique_id = generate_unique_id()
            callback.__unique_id__ = unique_id

        hook = InstanceHookSchema(
            hook_name=hook_table[1],
            callback=callback,
            component_type=hook_table[0],
            unique_id=unique_id,
        )
        logger.debug(f"[pne hook registry] instance hook: {hook}")
        cls.unmounted_hook_store.append(hook)

    @classmethod
    def unregister_hook(cls, callback: Callable):
        for hook in cls.component_hook_store:
            if id(hook.callback) == id(callback):
                cls.component_hook_store.remove(hook)
        for hook in cls.instance_hook_store:
            if id(hook.callback) == id(callback):
                cls.instance_hook_store.remove(hook)

    @classmethod
    def mount_instance_hook(cls, hook_callback: Callable, mounted_obj: object):
        for unmounted_hook in Hook.unmounted_hook_store:
            if (
                getattr(hook_callback, "__unique_id__", None)
                and unmounted_hook.unique_id == hook_callback.__unique_id__
            ):
                hook = unmounted_hook.copy()
                hook.mounted_obj = mounted_obj
                Hook.instance_hook_store.append(hook)
                Hook.unmounted_hook_store.remove(unmounted_hook)
                logger.debug(f"[pne hook mount] {hook}")
                return
        raise ValueError(
            f"Could not mount function <{hook_callback}> to {mounted_obj.__class__.__name__}. "  # noqa
            "You may have used component Hook, but component Hook cannot be mounted to an instance."  # noqa
        )

    @classmethod
    def get_hooks(cls, hook_name: str, mounted_obj: object) -> List[BaseHookSchema]:
        """Get relevant component hooks and instance hooks for mounted_obj from hook
        store."""
        return [
            *Hook._get_component_hooks(hook_name),
            *Hook._get_instance_hooks(hook_name, mounted_obj),
        ]

    @classmethod
    def _get_component_hooks(cls, hook_name: str) -> List[BaseHookSchema]:
        hooks: List[BaseHookSchema] = []
        for hook in cls.component_hook_store:
            if hook.hook_name == hook_name:
                hooks.append(hook)
        return hooks

    @classmethod
    def _get_instance_hooks(
        cls, hook_name: str, mounted_obj: object
    ) -> List[BaseHookSchema]:
        hooks: List[BaseHookSchema] = []
        for hook in cls.instance_hook_store:
            if hook.hook_name == hook_name and hook.mounted_obj is mounted_obj:
                hooks.append(hook)
        return hooks

    @classmethod
    def call_hook(cls, hook_table: Tuple, mounted_obj: object, *args, **kwargs):
        """Invoke the specified hook when specifying the component lifecycle."""
        hooks = cls.get_hooks(hook_table[1], mounted_obj)

        if hooks:
            logger.debug(
                f"[pne hook] hooks <{hook_table}> mounted_obj <{mounted_obj.__class__.__name__}> call hook: <{hooks}>"  # noqa
            )
            for hook in hooks:
                hook.callback(*args, **kwargs)
