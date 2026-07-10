"""
conversation_manager.py

Handles pending conversations.
"""

from app.models.conversation_state import ConversationState
from app.models.intent import Intent


class ConversationManager:

    def __init__(self) -> None:
        self._state = ConversationState()

    @property
    def active(self) -> bool:
        return self._state.active

    @property
    def state(self) -> ConversationState:
        return self._state

    def begin(self, intent: Intent, prompt: str,) -> None:

        self._state.active = True
        self._state.pending_intent = intent
        self._state.prompt = prompt

    def complete(self) -> None:
        self._state.clear()