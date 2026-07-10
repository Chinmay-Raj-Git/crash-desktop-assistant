from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.models.action_result import ActionResult
from app.models.intent import Intent


@dataclass(slots=True, frozen=True)
class AssistantResponse:
    """
    Final response returned by the assistant after processing
    a user request.

    This object hides whether the response came directly from the
    initial LLM response or from a generated failure explanation.
    """

    user_input: str

    assistant_message: str

    intent: Intent

    action_result: ActionResult

    metadata: dict[str, Any] = field(default_factory=dict)