"""
conversation_state.py

Represents an active multi-turn conversation.
"""

from dataclasses import dataclass

from app.models.intent import Intent


@dataclass(slots=True)
class ConversationState:
    """
    Stores information about a pending conversation.
    """

    # Whether we're waiting for the user's next reply
    active: bool = False

    # The original intent being completed
    pending_intent: Intent | None = None

    # Question currently asked to the user
    question: str = ""

    def clear(self) -> None:
        """
        Resets the conversation.
        """
        self.active = False
        self.pending_intent = None
        self.question = ""