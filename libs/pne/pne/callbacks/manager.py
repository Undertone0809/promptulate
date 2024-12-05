from typing import Any, List, Optional, Union

from pne.callbacks.base import CallbackHandler
from pne.message import BaseMessage, MessageSet
from pne.utils.logger import logger


class CallbackManager(CallbackHandler):
    """
    Manages multiple callback handlers and provides a unified interface.

    Implements the Composite pattern to act as both a handler and a manager of handlers.
    """

    def __init__(
        self,
        callbacks: Optional[List[CallbackHandler]] = None,
        raise_error: bool = False,
    ) -> None:
        """
        Initialize the callback manager with optional handlers.

        Args:
            callbacks: A list of callback handlers to manage. Defaults to an empty list.
            raise_error: Whether to raise errors in handlers. Defaults to False.
        """
        super().__init__(raise_error=raise_error)
        self._handlers: List[CallbackHandler] = callbacks or []

    @property
    def handlers(self) -> List[CallbackHandler]:
        """Returns the list of managed handlers."""
        return self._handlers

    def add_handler(self, handler: CallbackHandler) -> None:
        """Adds a handler to the manager."""
        if handler not in self._handlers:
            self._handlers.append(handler)
        else:
            logger.warning(f"Handler {handler} is already added.")

    def remove_handler(self, handler: CallbackHandler) -> None:
        """Removes a handler from the manager."""
        try:
            self._handlers.remove(handler)
        except ValueError:
            logger.warning(f"Handler {handler} not found in the manager.")

    def _execute_handler_method(
        self, method_name: str, handler: CallbackHandler, **kwargs: Any
    ) -> None:
        """
        Executes a specific method on a handler and handles exceptions.

        Args:
            method_name: The name of the method to execute.
            handler: The handler on which to execute the method.
            kwargs: The arguments to pass to the method.
        """
        try:
            getattr(handler, method_name)(**kwargs)
        except Exception as e:
            logger.error(f"Error in {method_name} of handler {handler}: {e}")
            if self.raise_error:
                raise

    def on_llm_start(
        self,
        messages: MessageSet,
        **kwargs: Any,
    ) -> None:
        """Triggers the `on_llm_start` method for all handlers."""
        for handler in self.handlers:
            self._execute_handler_method(
                "on_llm_start", handler, messages=messages, **kwargs
            )

    def on_llm_new_token(
        self,
        token: str,
        **kwargs: Any,
    ) -> None:
        """Triggers the `on_llm_new_token` method for all handlers."""
        for handler in self.handlers:
            self._execute_handler_method(
                "on_llm_new_token", handler, token=token, **kwargs
            )

    def on_llm_end(
        self,
        response: BaseMessage,
        **kwargs: Any,
    ) -> None:
        """Triggers the `on_llm_end` method for all handlers."""
        for handler in self.handlers:
            self._execute_handler_method(
                "on_llm_end", handler, response=response, **kwargs
            )

    def on_llm_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        **kwargs: Any,
    ) -> None:
        """Triggers the `on_llm_error` method for all handlers."""
        for handler in self.handlers:
            self._execute_handler_method("on_llm_error", handler, error=error, **kwargs)
