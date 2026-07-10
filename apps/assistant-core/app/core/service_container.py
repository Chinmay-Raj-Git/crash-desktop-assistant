"""
service_container.py

A lightweight Dependency Injection (DI) container.

The ServiceContainer is responsible for storing and providing
shared singleton services throughout the assistant.

Examples:
    - Logger
    - Configuration Provider
    - LLM Provider
    - Plugin Registry

Instead of creating services everywhere, modules request them
from this container.
"""

from typing import Any


class ServiceContainer:
    """
    Simple singleton service registry.
    """

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """
        Registers a singleton service.

        Raises:
            ValueError:
                If the service name already exists.
        """
        if name in self._services:
            raise ValueError(f"Service '{name}' is already registered.")

        self._services[name] = service

    def resolve(self, name: str) -> Any:
        """
        Retrieves a registered service.

        Raises:
            KeyError:
                If the service doesn't exist.
        """
        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered.")

        return self._services[name]

    def is_registered(self, name: str) -> bool:
        """
        Checks whether a service exists.
        """
        return name in self._services

    def unregister(self, name: str) -> None:
        """
        Removes a registered service.
        """
        self._services.pop(name, None)

    def clear(self) -> None:
        """
        Removes all registered services.
        """
        self._services.clear()

    @property
    def services(self) -> tuple[str, ...]:
        """
        Returns the names of all registered services.
        """
        return tuple(sorted(self._services.keys()))