"""
mock_llm_provider.py

Temporary LLM implementation.

Used until a real OpenAI provider
is integrated.
"""

from app.interfaces.llm_provider import ILLMProvider
from app.models.action_result import ActionResult
from app.models.intent import Intent
from app.services.intent_parser import IntentParser


class MockLLMProvider(ILLMProvider):
    
    def __init__(self, parser: IntentParser, capability_context: str,) -> None:

        self._parser = parser
        self._capability_context = capability_context

    def parse_intent(self, user_input: str,) -> tuple[Intent, str]:

        intent = self._parser.parse(user_input)
        command = user_input.lower()

        # if "open brave" in command:

        #     return (
        #         Intent(
        #             plugin="application",
        #             action="launch",
        #             target="Brave Browser",
        #             original_input=user_input,
        #         ),

        #         "Brave Browser opened sir.",
        #     )
            
        # if "close brave" in command:

        #     return (
        #         Intent(
        #             plugin="application",
        #             action="close",
        #             target="Brave Browser",
        #             original_input=user_input,
        #         ),

        #         "Brave Browser closed sir.",
        #     )
            
        # if "is brave running" in command:

        #     return (
        #         Intent(
        #             plugin="application",
        #             action="running",
        #             target="Brave Browser",
        #             original_input=user_input,
        #         ),

        #         "Brave is running sir.",
        #     )
            
        response = {
            "launch": "Opening application sir.",
            "close": "Closing application sir.",
            "running": "Yes its running sir.",
            "open_url": "Opening the requested URL sir.",
        }[intent.action]

        return intent, response

        raise NotImplementedError(
            "Mock provider only supports Brave for now."
        )

    def generate_failure_response(self, user_input: str, result: ActionResult, personality: str,) -> str:

        return (
            f"Sorry, I couldn't complete that request.\n"
            f"Reason: {result.message}"
        )