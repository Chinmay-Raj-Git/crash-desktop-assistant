"""
conversation_manager.py

Handles pending conversations.
"""

from app.models.execution_plan import ExecutionPlan
from app.models.execution_plan import PlannedTask


class ConversationManager:

    def __init__(self) -> None:
        self.active = False
        self.pending_plan = ExecutionPlan("", ())
        self.next_task_index = -1
        self.confirmation_question = ""

    # @property
    # def active(self) -> bool:
    #     return self.active
    #  THIS THING CURRENTLY THROWS AN AttributeError: property 'active' of 'ConversationManager' object has no setter
        
    def store_pending_plan(self, pending_plan: ExecutionPlan, next_task_index: int, confirmation_question: str,) -> None:
        """
        Pause an execution plan until the user provides
        additional input.
        """

        self.active = True
        self.pending_plan = pending_plan
        self.next_task_index = next_task_index
        self.confirmation_question = confirmation_question

    def complete(self) -> None:
        self.active = False
        self.pending_plan = ExecutionPlan("", ())
        self.next_task_index = -1
        self.confirmation_question = ""