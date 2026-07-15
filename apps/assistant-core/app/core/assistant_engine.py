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
        intent = Intent(plugin="", action="")
        assistant_message = ""
        
        # Check if there's an active conversation awaiting user confirmation
        if self._conversation_manager.active:
            pending_intent = self._conversation_manager.state.pending_intent
            
            if pending_intent is None:
                self._logger.error("No pending intent found in conversation state.")
                return AssistantResponse(
                    user_input=user_input, assistant_message="Error: No pending intent found.",
                    intent=Intent(plugin="", action=""), action_result=ActionResult(status=ActionStatus.FAILED, message="No pending intent found.", error="No pending intent",),
                )
                
            # Process the user's response to the confirmation question
            if user_input.lower() in ["yes", "y"]:
                # User confirmed the action
                self._logger.info(f"User confirmed the action for intent: {pending_intent}")
                action_result = self._dispatcher.dispatch(pending_intent, skip_confirmation=True,)
                assistant_message = "Action executed upon confirmation."
                
                self._conversation_manager.complete()                
            
            elif user_input.lower() in ["no", "n"]:
                # User denied the action
                self._logger.info(f"User denied the action for intent: {pending_intent}")
                
                self._conversation_manager.complete()
                
                return AssistantResponse(
                    user_input=user_input, assistant_message="Action cancelled.",
                    intent=pending_intent, action_result=ActionResult(status=ActionStatus.FAILED, message="Action cancelled.", error="User denied the action",),
                )
                
            else:
                # User provided an invalid response
                self._logger.warning(f"Invalid response to confirmation question: {user_input}")
                return AssistantResponse(
                    user_input=user_input, assistant_message="Error: Invalid response.",
                    intent=Intent(plugin="", action=""), action_result=ActionResult(status=ActionStatus.FAILED, message="Invalid response.", error="Invalid response",),
                )
                
        # No active convos, parse normally
        else:                   
            intent, initial_response = self._llm.parse_intent(user_input)
            
            action_result = self._dispatcher.dispatch(intent)            
            assistant_message = initial_response
            
            if(action_result.status == ActionStatus.UNCONFIRMED):
                assistant_message = action_result.message
                self._conversation_manager.store_pending(intent, assistant_message)
            
            
        if action_result.status == ActionStatus.FAILED:
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