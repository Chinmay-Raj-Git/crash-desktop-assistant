"""
response_context.py

Contains all information required by the ResponseEngine
to generate the final assistant response.
"""

from dataclasses import dataclass

from app.models.action_result import ActionResult
from app.models.intent import Intent


@dataclass(slots=True)
class ResponseContext:
    """
    Context passed to the ResponseEngine.
    """

    # Original user message
    user_input: str

    # Parsed intent
    intent: Intent

    # Result returned by the plugin
    result: ActionResult

    # Initial assistant response from LLM #1
    initial_response: str

    # Active personality prompt/profile
    personality: str