from __future__ import annotations

from app.interfaces.llm_provider import ILLMProvider
from app.interfaces.logger import ILogger
from app.models.action_result import ActionStatus
from app.models.action_result import ActionResult
from app.models.assistant_response import AssistantResponse
from app.models.execution_plan import ExecutionPlan
from app.models.intent import Intent, IntentStatus
from app.models.planned_task import PlannedTask
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
            # return self._continue_conversation(user_input)

        return self._execute_plan(user_input)
    
    def _execute_plan(self, user_input: str) -> AssistantResponse:
        
        plan = self._llm.parse_execution_plan(user_input)
        
        #                                       DEBUG
        print("================================================================================================")
        print("================-----------------------------------------------------------------==============")
        print("SUM. RESPONSE: " + plan.summary_response)
        print("Tasks:")
        for task in plan.tasks:
            print("- 0" + str(task.task_id))
            print("- " + str(task.intent))
            print("- " + task.response + "\n-=-=-=-=-=-=-=-=-=-")
        print("================-----------------------------------------------------------------==============")
        print("================================================================================================")
        #                                       DEBUG
        
        last_result = ActionResult(
            status=ActionStatus.SUCCESS,
            message="DEFAULT",
            data={},
        )
        
        summary_response = plan.summary_response

        for index, task in enumerate(plan.tasks):
            last_result = self._dispatcher.dispatch(task.intent)
            print("==> "+last_result.message)

            if last_result.status == ActionStatus.FAILED:
                break
            if last_result.status == ActionStatus.UNCONFIRMED:
                self._conversation_manager.store_pending_plan(pending_plan=plan, next_task_index=index, confirmation_question=last_result.message)
                self._continue_conversation()            
            
        return AssistantResponse(user_input=user_input, assistant_message=summary_response, intent=Intent(plugin="", action=""), action_result=last_result)
    
    def _continue_conversation(self):
        plan = self._conversation_manager.pending_plan
        task_idx = self._conversation_manager.next_task_index
        task = plan.tasks[task_idx]
        confirmation_question = self._conversation_manager.confirmation_question
        
        print(">>> " + confirmation_question)
        
        proceed = ["y", "yes"]
        abort = ["n", "no"]
        
        while(True):
            convo_input = input("> ").strip()
            
            if(convo_input.lower() in proceed):
                self._dispatcher.dispatch(task.intent, skip_confirmation = True)
                self._conversation_manager.complete()
                return
            elif(convo_input.lower() in abort):
                self._conversation_manager.complete()
                return
                