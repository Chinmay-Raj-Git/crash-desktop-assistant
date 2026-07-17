from __future__ import annotations

from app.interfaces.llm_provider import ILLMProvider
from app.interfaces.logger import ILogger
from app.models.action_result import ActionStatus
from app.models.action_result import ActionResult
from app.models.assistant_response import AssistantResponse
from app.models.intent import Intent, IntentStatus
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
        # TODO:
        # Re-enable once ExecutionPlan-based confirmation
        # workflow is implemented.

        # if self._conversation_manager.active:
        #     return self._continue_conversation(user_input)

        return self._execute_plan(user_input)
    
    def _execute_plan(self, user_input: str) -> AssistantResponse:
        
        plan = self._llm.parse_execution_plan(user_input)
        print("================================================================================================")
        print("================-----------------------------------------------------------------==============")
        print(plan)
        print("================-----------------------------------------------------------------==============")
        print("================================================================================================")
        last_result = ActionResult(
            status=ActionStatus.SUCCESS,
            message="DEFAULT",
            data={},
        )
        
        assistant_message = plan.summary_response

        for task in plan.tasks:

            last_result = self._dispatcher.dispatch(task.intent)
            print("==> "+last_result.message)

            if last_result.status == ActionStatus.FAILED:
                break
            if last_result.status == ActionStatus.UNCONFIRMED:
                break
            
            
        return AssistantResponse(user_input=user_input, assistant_message=assistant_message, intent=Intent(plugin="", action=""), action_result=last_result)