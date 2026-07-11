"""
gemini_provider.py

Production implementation of ILLMProvider using
Google Gemini.

Responsible only for communication with Gemini and
conversion between JSON responses and domain models.
"""

from __future__ import annotations

import json

from google import genai

from app.interfaces.llm_provider import ILLMProvider

from app.models.intent import Intent
from app.models.llm_intent_schema import (INTENT_SCHEMA, INTENT_RULES, RESPONSE_MESSAGE_EXAMPLES, USAGE_EXAMPLES,)


class GeminiProvider(ILLMProvider):

    def __init__(self, api_key: str, model: str, capability_context: str,) -> None:

        self._client = genai.Client(api_key=api_key,)
        self._model = model
        self._capability_context = capability_context

    # ---------------------------------------------------------

    def parse_intent(self, user_input: str,):

        prompt = self._build_intent_prompt(user_input,)
        response = self._client.models.generate_content(model=self._model, contents=prompt,)
        
        text = ""
        if(response and response.text):
            text = response.text.strip()
        
        intent = Intent(plugin="", action="", target="", parameters={}, original_input=user_input,)
        try:
            data = json.loads(text)
            intent = Intent(plugin=data["plugin"], action=data["action"], target=data.get("target"),
                parameters=data.get("parameters",{},), original_input=user_input,
            )
            return (intent, data["response"],)

        except json.JSONDecodeError:
            print(f"Failed to parse JSON from Gemini response: \n{text}")
            return (intent, "Failed to parse Gemini response.",)



    # ---------------------------------------------------------

    def generate_failure_response(self, user_input, result, personality,):

        prompt = self._build_failure_prompt(user_input, result, personality,)

        response = self._client.models.generate_content(model=self._model, contents=prompt,)

        return response.text

    # ---------------------------------------------------------

    def _build_intent_prompt(self, user_input: str,) -> str:

        return f"""
        -YOUR ROLE-

        You are the intent extraction engine for an AI-powered
        Windows desktop assistant.

        You are NOT the assistant that executes commands.

        Your responsibility is ONLY to:

        1. Understand the user's request.

        2. Convert it into structured JSON.

        3. Generate the short assistant response that should be
        shown immediately IF execution succeeds.

        You NEVER execute commands.

        You NEVER mention limitations like:

        "I can't access your computer."

        "I cannot launch applications."

        "I don't have permission."

        The desktop assistant executes commands after receiving
        your structured output.
        
        ...
        
        -AVAILABLE CAPABILITIES-
        {self._capability_context}

        ...

        -JSON SCHEMA-
        {INTENT_SCHEMA}

        ...

        -RULES-
        {INTENT_RULES}

        ...

        -EXAMPLES-
        {USAGE_EXAMPLES}
        ----------
        {RESPONSE_MESSAGE_EXAMPLES}

        ...

        -USER REQUEST-
        {user_input}
        
        ...

        """
        
    def _build_failure_prompt(self, user_input: str, result, personality: str,) -> str:

        return f"""
        -YOUR ROLE-

        You are the failure response engine for an AI-powered
        Windows desktop assistant.

        You are NOT the assistant that executes commands.

        Your responsibility is ONLY to:

        1. Understand the user's request.

        2. Understand the failure result.

        3. Generate a natural language response that should be
        shown immediately to the user.

        You NEVER execute commands.

        You NEVER mention limitations like:

        "I can't access your computer."

        "I cannot launch applications."

        "I don't have permission."

        The desktop assistant executes commands after receiving
        your structured output.
        
        ...
        
        -USER REQUEST-
        {user_input}

        ...

        -FAILURE RESULT-
        {result.message}

        ...

        -TECHNICAL ERROR-
        {result.error}

        ...
        
        """