"""
logger.py

Defines the logging interface used throughout the assistant.

The rest of the application should depend on this interface
instead of Python's logging module directly.
"""

from abc import ABC, abstractmethod
from typing import Any


class ILogger(ABC):
    """
    Base logger contract.
    """

    @abstractmethod
    def debug(self, message: str, **context: Any) -> None:
        """
        Logs debug information.
        """
        raise NotImplementedError

    @abstractmethod
    def info(self, message: str, **context: Any) -> None:
        """
        Logs informational events.
        """
        raise NotImplementedError

    @abstractmethod
    def warning(self, message: str, **context: Any) -> None:
        """
        Logs warnings.
        """
        raise NotImplementedError

    @abstractmethod
    def error(self, message: str, **context: Any) -> None:
        """
        Logs errors.
        """
        raise NotImplementedError

    @abstractmethod
    def critical(self, message: str, **context: Any) -> None:
        """
        Logs critical failures.
        """
        raise NotImplementedError