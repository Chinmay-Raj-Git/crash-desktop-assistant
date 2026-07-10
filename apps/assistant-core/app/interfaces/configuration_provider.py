"""
configuration_provider.py

Defines how configuration is accessed throughout the assistant.

Implementations may read configuration from:

- JSON
- TOML
- Environment variables
- SQLite
"""

from abc import ABC, abstractmethod
from typing import Any


class IConfigurationProvider(ABC):
    """
    Base configuration provider.
    """

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """
        Returns a configuration value.

        Example:

            provider.get("assistant.name")
        """
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Updates a configuration value.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self) -> None:
        """
        Persists configuration.
        """
        raise NotImplementedError

    @abstractmethod
    def reload(self) -> None:
        """
        Reloads configuration from storage.
        """
        raise NotImplementedError