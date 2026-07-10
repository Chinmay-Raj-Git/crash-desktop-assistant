"""
capability.py

Defines the Capability model.

A Capability represents a single operation that a plugin can perform.

Examples:
    application.launch
    application.close
    browser.search
    filesystem.copy

Capabilities are registered during startup and become the single source
of truth for what the assistant is allowed to execute.
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Capability:
    """
    Represents one executable capability exposed by a plugin.
    """

    # Plugin that owns this capability
    plugin: str

    # Name of the action
    action: str

    # Human-readable description
    description: str

    # Whether this action requires confirmation
    requires_confirmation: bool = False

    @property
    def id(self) -> str:
        """
        Unique capability identifier.

        Example:
            application.launch
        """
        return f"{self.plugin}.{self.action}"

    def __str__(self) -> str:
        return self.id