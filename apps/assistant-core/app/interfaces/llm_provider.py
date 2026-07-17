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
from app.models.execution_plan import ExecutionPlan


class ILLMProvider(ABC):
    """
    Produces structured execution plans from natural language.

    Implementations are responsible only for planning.

    They never execute actions.
    """

    @abstractmethod
    def parse_execution_plan(self, user_input: str,) -> ExecutionPlan:
        """
        Convert a natural-language request into an
        ordered ExecutionPlan.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_failure_response(self, user_input: str, result: ActionResult, personality: str,) -> str | None :
        """
        Generates a conversational response after a failed
        or partially successful task.
        """
        raise NotImplementedError