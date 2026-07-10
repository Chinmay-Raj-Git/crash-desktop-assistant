"""
response_engine.py

Determines the final response shown to the user.
"""

from app.interfaces.llm_provider import ILLMProvider
from app.models.action_result import ActionStatus
from app.models.response_context import ResponseContext


class ResponseEngine:

    def __init__(self, llm_provider: ILLMProvider,) -> None:

        self._llm = llm_provider

    def generate(self, context: ResponseContext, ) -> str:
        """
        Generates the final assistant response.

        Success:
            Uses the response already generated
            by the first LLM call.

        Failure/Partial:
            Calls the LLM again with
            ActionResult details.
        """

        if context.result.status == ActionStatus.SUCCESS:
            return context.initial_response

        return self._llm.generate_failure_response(
            user_input=context.user_input,
            result=context.result,
            personality=context.personality,
        )