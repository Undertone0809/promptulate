from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from pne.message import MessageSet


class CallbackHandler(ABC):
    """Base callback handler that can be used to handle callbacks from different
    chains."""

    def __init__(self, raise_error: bool = False) -> None:
        """Initialize callback handler.

        Args:
            raise_error: If True, errors in callbacks will be raised instead of being
            caught. Default is False, which means errors will be caught silently.
        """
        self._raise_error = raise_error

    @property
    def raise_error(self) -> bool:
        """Whether to raise errors in callbacks."""
        return self._raise_error

    def on_llm_start(
        self,
        messages: MessageSet,
        **kwargs: Any,
    ) -> None:
        """Run when LLM starts running."""
        pass

    def on_llm_new_token(
        self,
        token: str,
        **kwargs: Any,
    ) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        pass

    def on_llm_end(
        self,
        response: Any,
        **kwargs: Any,
    ) -> None:
        """Run when LLM ends running."""
        pass

    def on_llm_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        **kwargs: Any,
    ) -> None:
        """Run when LLM errors."""
        pass
