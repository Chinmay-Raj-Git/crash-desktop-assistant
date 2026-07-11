"""
browser_plugin.py

Handles all browser and webpage capabilities.

The dispatcher routes every intent whose plugin is
'browser' to this plugin.

Here LLM is responsible for generating the appropriate URL based on the intent.

The plugin then dispatches internally based on the
requested action.
"""

from __future__ import annotations

from pathlib import Path
import webbrowser

from app.models.action_result import ActionResult
from app.models.action_result import ActionStatus
from app.models.capability import Capability
from app.models.intent import Intent
from app.models.plugin_metadata import PluginMetadata

from app.services.process_service import ProcessService
from app.services.resource_registry import ResourceRegistry

from plugins.base_plugin import BasePlugin


class BrowserPlugin(BasePlugin):

    def __init__(self, registry: ResourceRegistry, process_service: ProcessService,) -> None:

        
        self._metadata = self._load_metadata(
            path=Path(__file__).parent / "plugin.json",
            capabilities=(
                    Capability(plugin="browser", action="open_url", description="Open a URL in the default browser",),
                ),
        )
        
        super().__init__(metadata=self._metadata)

        self._registry = registry
        self._process_service = process_service

    @property
    def metadata(self) -> PluginMetadata:
        return self._metadata

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health_check(self) -> bool:
        return True

    def execute(self, intent: Intent,) -> ActionResult:

        match intent.action:

            case "open_url":
                return self._open_url(intent)
            
            case _:
                return ActionResult(
                    status=ActionStatus.FAILED,
                    message=f"Unsupported browser action '{intent.action}'.",
                )
    
    # ---------------------------------------------------------
    
    def _open_url(self, intent: Intent, ) -> ActionResult:
        url = intent.target

        if not url:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="No URL supplied.",
            )

        webbrowser.open(url)

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message="Website opened.",
            data={
                "url": url,
            },
        )