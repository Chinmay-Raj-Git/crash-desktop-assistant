"""
intent_parser.py

Simple rule-based intent parser used by the mock LLM provider.

This parser exists only for local development and testing.
It intentionally shares the same output contract as future
cloud LLM providers.
"""

from __future__ import annotations

from app.models.application_resource import ApplicationResource
from app.models.intent import Intent
from app.services.resource_registry import ResourceRegistry


class IntentParser:

    def __init__(self, resource_registry: ResourceRegistry,) -> None:

        self._registry = resource_registry

    def parse(self, user_input: str,) -> Intent:

        text = user_input.lower()

        action = self._detect_action(text)

        # if action is None:
        #     return None

        target_entity = self._detect_application(text)

        # if application is None:
            # return None

        return Intent(
            plugin= text.split()[0] == "web" and "browser" or "application",
            action=action,
            target=target_entity.display_name,
            original_input=user_input,
        )

    # ---------------------------------------------------------

    def _detect_action(self, text: str,) -> str:

        launch = {"launch", "start", "run",}

        close = {"close", "quit", "exit", "terminate", "kill",}

        running = {"running", "opened", "open?", "active",}
        
        open_url = {"web", "open", "go to", "navigate to", "visit", "browse",}

        words = set(text.split())

        if words & launch:
            return "launch"

        if words & close:
            return "close"

        if words & running:
            return "running"
        
        if words & open_url:
            return "open_url"

        return ""

    # ---------------------------------------------------------

    def _detect_application(self, text: str,) -> ApplicationResource:
        
        if(text.split()[0] == "web"):
            return ApplicationResource(
                id="web",
                # display_name here identifies "https" in text and that whole string url is saved in display_name, so that it can be used in the browser plugin to open the url
                display_name=next((string for string in text.split() if string.startswith("https") or string.startswith("http")), "web"),
                executable="",
                process_name="",
                aliases=("web", "browser", "chrome", "firefox", "edge", "safari",),
            )

        for app in self._registry.applications:

            for alias in app.aliases:

                if alias.lower() in text:
                    return app

        return ApplicationResource(id="unknown", display_name="Unknown Application", executable="", process_name="", aliases=(),)