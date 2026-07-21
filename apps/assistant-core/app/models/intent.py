"""
intent.py

Defines the standardized Intent model used throughout the assistant.

Every user request—whether from text, voice, or another input source—is
converted into an Intent before execution.

The Intent is the contract between the AI reasoning layer and the plugin
execution layer.

The AI determines *what* the user wants.

Plugins determine *how* to perform it.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IntentStatus(Enum):
    """
    Represents the lifecycle state of an intent.
    """

    PENDING = "pending"
    VALIDATED = "validated"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class Intent:
    """
    Represents a structured command produced by the AI.

    Example
    -------
    User:
        "Open Visual Studio Code"

    Intent:
        plugin = "application"
        action = "launch"
        target = "Visual Studio Code"
        parameters = {}
    """

    # Which plugin should execute this intent?
    plugin: str

    # Action to perform
    action: str

    # Primary object of the action
    target: str | None = None

    # Optional arguments
    parameters: dict[str, Any] = field(default_factory=dict)

    # Current execution status
    status: IntentStatus = IntentStatus.PENDING

    # Original user input (useful for logs/debugging)
    original_input: str = ""

    def update_status(self, status: IntentStatus) -> None:
        """
        Updates the current execution status.
        """
        self.status = status

    @property
    def capability(self) -> str:
        """
        Returns the capability string used by the dispatcher.

        Example:
            application.launch
            browser.search
            filesystem.copy
        """
        return f"{self.plugin}.{self.action}"

    def __str__(self) -> str:
        """
        Human-readable representation.
        """
        return (
            f"Intent("
            f"plugin='{self.plugin}', "
            f"action='{self.action}', "
            f"target='{self.target}', "
            f"parameters={self.parameters}, "
            f"status='{self.status.value}')"
        )