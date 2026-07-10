"""
event_bus.py

Implements a lightweight synchronous Event Bus.

The EventBus allows components to communicate without
knowing about each other directly.

Example:

Plugin finishes execution
        │
        ▼
Publishes "plugin.executed"

Logger listens

UI listens

Metrics listens
"""

from collections import defaultdict
from collections.abc import Callable
from typing import Any


EventHandler = Callable[..., None]


class EventBus:
    """
    Lightweight publish-subscribe event system.
    """

    def __init__(self) -> None:
        self._listeners: dict[
            str,
            list[EventHandler],
        ] = defaultdict(list)

    def subscribe(
        self,
        event: str,
        handler: EventHandler,
    ) -> None:
        """
        Registers an event listener.
        """
        self._listeners[event].append(handler)

    def unsubscribe(
        self,
        event: str,
        handler: EventHandler,
    ) -> None:
        """
        Removes an event listener.
        """
        if handler in self._listeners[event]:
            self._listeners[event].remove(handler)

    def publish(
        self,
        event: str,
        **payload: Any,
    ) -> None:
        """
        Publishes an event to all listeners.
        """
        for handler in self._listeners[event]:
            handler(**payload)