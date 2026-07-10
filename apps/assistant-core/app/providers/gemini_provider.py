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


class GeminiProvider(ILLMProvider):

    def __init__(self, api_key: str, model: str, capability_context: str,) -> None:

        self._client = genai.Client(api_key=api_key,)
        self._model = model
        self._capability_context = capability_context

    # ---------------------------------------------------------

    def parse_intent(self, user_input: str,):

        prompt = self._build_prompt(user_input,)
        response = self._client.models.generate_content(model=self._model, contents=prompt,)
        
        text = ""
        if(response and response.text):
            text = response.text.strip()
        data = json.loads(text)

        intent = Intent(plugin=data["plugin"], action=data["action"], target=data.get("target"),
            parameters=data.get("parameters",{},), original_input=user_input,
        )

        return (intent, data["response"],)

    # ---------------------------------------------------------

    def generate_failure_response(self, user_input, result, personality,):

        prompt = f"""
            The assistant failed.

            User:
            {user_input}

            Failure:
            {result.message}

            Technical error:
            {result.error}

            Respond naturally as

            {personality}
            """

        response = self._client.models.generate_content(model=self._model, contents=prompt,)

        return response.text

    # ---------------------------------------------------------

    def _build_prompt(self, user_input: str,) -> str:

        return f"""
            You are an intent parser for a desktop assistant.

            {self._capability_context}

            Rules

            1. Return ONLY JSON.

            2. Never wrap JSON in markdown.

            3. Never explain.

            4. Use only available plugins.

            5. Use only available actions.

            6. For browser URLs, return the COMPLETE URL.

            7. If the user asks to search, generate the full search URL.

            8. Return this schema

            {{
                "plugin":"",
                "action":"",
                "target":"",
                "parameters":{{}},
                "response":""
            }}

            User request

            {user_input}
        """