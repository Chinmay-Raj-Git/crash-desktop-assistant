"""
llm_provider.py

Defines the interface for every Large Language Model provider.

Examples:
    OpenAI
    Gemini
    Claude
    Azure OpenAI
"""

from abc import ABC, abstractmethod

from app.models.action_result import ActionResult
from app.models.intent import Intent


class ILLMProvider(ABC):
    """
    Contract implemented by every AI provider.
    """

    @abstractmethod
    def parse_intent(
        self,
        user_input: str,
    ) -> tuple[Intent, str]:
        """
        Converts a natural language request into:

        1. Structured Intent
        2. Initial assistant response

        Example

        User:
            "Open Brave"

        Returns:

        (
            Intent(...),
            "Opening Brave for you."
        )
        """
        raise NotImplementedError

    @abstractmethod
    def generate_failure_response(
        self,
        user_input: str,
        result: ActionResult,
        personality: str,
    ) -> str:
        """
        Generates a conversational response after a failed
        or partially successful task.
        """
        raise NotImplementedError