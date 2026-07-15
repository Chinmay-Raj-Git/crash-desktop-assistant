"""
action_result.py

Represents the outcome of a plugin execution.

Every plugin returns an ActionResult regardless of success or failure.

This standardizes communication between plugins, logging,
and the Response Engine.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ActionStatus(Enum):
    """
    Execution outcome.
    """

    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    UNCONFIRMED = "unconfirmed"


@dataclass(slots=True)
class ActionResult:
    """
    Standard result returned by every plugin.
    """

    # Overall execution status
    status: ActionStatus

    # Human-readable technical message
    message: str

    # Optional structured payload
    data: dict[str, Any] = field(default_factory=dict)

    # Technical error information
    error: str | None = None

    # Suggested recovery or next step
    suggestion: str | None = None

    # Execution time in seconds
    execution_time: float = 0.0

    @property
    def success(self) -> bool:
        """
        Convenience property.
        """
        return self.status == ActionStatus.SUCCESS

    def __bool__(self) -> bool:
        """
        Allows:

        if result:
            ...
        """
        return self.success

    def __str__(self) -> str:
        return (
            f"ActionResult("
            f"status={self.status.value}, "
            f"message='{self.message}')"
        )