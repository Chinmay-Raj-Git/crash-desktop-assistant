from __future__ import annotations

from app.interfaces.llm_provider import ILLMProvider
from app.interfaces.logger import ILogger
from app.models.action_result import ActionStatus
from app.models.assistant_response import AssistantResponse
from app.models.intent import IntentStatus
from app.models.response_context import ResponseContext
from app.core.command_dispatcher import CommandDispatcher
from app.core.response_engine import ResponseEngine
from app.core.conversation_manager import ConversationManager


class AssistantEngine:
    """
    High-level orchestration service.

    Coordinates the complete assistant pipeline while keeping
    the UI layer unaware of implementation details.

    Flow

    User Input
        ↓
    LLM
        ↓
    Dispatcher
        ↓
    Plugins
        ↓
    Response Engine
        ↓
    AssistantResponse
    """

    def __init__(self, llm: ILLMProvider, dispatcher: CommandDispatcher, response_engine: ResponseEngine,
        conversation_manager: ConversationManager, logger: ILogger,) -> None:
        self._llm = llm
        self._dispatcher = dispatcher
        self._response_engine = response_engine
        self._conversation_manager = conversation_manager
        self._logger = logger

    def process(self, user_input: str) -> AssistantResponse:
        self._logger.info(f"User: {user_input}")

        intent, initial_response = self._llm.parse_intent(user_input)
        # print("\nIntent Captured:", intent, "\nInitial Response:", initial_response, "\n")

        action_result = self._dispatcher.dispatch(intent)
        
        assistant_message = initial_response
        if(action_result.status != ActionStatus.SUCCESS):
            assistant_message = self._llm.generate_failure_response(user_input=user_input, result=action_result,
                personality="Professional"  # TODO: Make this dynamic based on user settings
            )

        self._logger.info(
            f"Execution finished: {action_result.status.value}"
        )

        return AssistantResponse(
            user_input=user_input, assistant_message=assistant_message or "Response Failed!",
            intent=intent, action_result=action_result,
        )