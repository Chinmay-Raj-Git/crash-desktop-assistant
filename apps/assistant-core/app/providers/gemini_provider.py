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
from app.models.planned_task import PlannedTask
from app.models.execution_plan import ExecutionPlan
from app.models.llm_intent_schema import (SYSTEM_ROLE, EXECUTION_PLAN_SCHEMA, RULES, PLANNING_RULES, RESPONSE_RULES, EXAMPLES)


class GeminiProvider(ILLMProvider):

    def __init__(self, api_key: str, model: str, capability_context: str,) -> None:

        self._client = genai.Client(api_key=api_key,)
        self._model = model
        self._capability_context = capability_context

    # ---------------------------------------------------------

    def parse_execution_plan(self, user_input: str,):

        prompt = self._build_intent_prompt(user_input,)
        response = self._client.models.generate_content(model=self._model, contents=prompt,)
        
        text = ""
        if(response and response.text):
            text = response.text.strip()
        
        intent = Intent(plugin="", action="", target="", parameters={}, original_input=user_input,)
        try:
            data = json.loads(text)
            tasks = []
            
            for task_data in data["tasks"]:
                intent_data = task_data["intent"]

                intent = Intent(
                    plugin=intent_data["plugin"],
                    action=intent_data["action"],
                    target=intent_data["target"],
                    parameters=intent_data.get("parameters", {}),
                    original_input=intent_data.get(
                        "original_input",
                        user_input,
                    ),
                )

                tasks.append(
                    PlannedTask(
                        task_id=task_data["task_id"],
                        intent=intent,
                        response=task_data["response"],
                    )
                )
                
                
            return ExecutionPlan(summary_response=data["summary_response"], tasks=tuple(tasks),)

        except json.JSONDecodeError:
            print(f"Failed to parse JSON from Gemini response: \n{text}")
            raise RuntimeError("Gemini returned invalid ExecutionPlan JSON.")



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

        {SYSTEM_ROLE}
        
        ...
        
        {EXECUTION_PLAN_SCHEMA}

        ...
        
        {RULES}
        
        ...
        
        {PLANNING_RULES}
        
        ...
        
        {RESPONSE_RULES}
        
        ...
        
        {EXAMPLES}

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