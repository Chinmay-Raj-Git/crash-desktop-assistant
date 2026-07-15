"""
application_plugin.py

Handles all desktop application capabilities.

The dispatcher routes every intent whose plugin is
'application' to this plugin.

The plugin then dispatches internally based on the
requested action.
"""

from __future__ import annotations

from pathlib import Path

from app.models.action_result import ActionResult
from app.models.action_result import ActionStatus
from app.models.capability import Capability
from app.models.intent import Intent
from app.models.plugin_metadata import PluginMetadata

from app.services.process_service import ProcessService
from app.services.resource_registry import ResourceRegistry

from plugins.base_plugin import BasePlugin


class ApplicationPlugin(BasePlugin):

    def __init__(self, registry: ResourceRegistry, process_service: ProcessService,) -> None:

        
        self._metadata = self._load_metadata(
            path=Path(__file__).parent / "plugin.json",
            capabilities=(
                    Capability(plugin="application", action="launch", description="Launch an application",),
                    Capability(plugin="application", action="close", description="Close an application", requires_confirmation=True,),
                    Capability(plugin="application", action="running", description="Check if an application is running",),
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

            case "launch":
                return self._launch(intent)

            case "close":
                return self._close(intent)

            case "running":
                return self._running(intent)

            case _:
                return ActionResult(
                    status=ActionStatus.FAILED,
                    message=f"Unsupported application action '{intent.action}'.",
                )

    # ---------------------------------------------------------

    def _launch(self, intent: Intent, ) -> ActionResult:

        app = self._registry.resolve_application(intent.target or "")

        if app is None:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Unknown application.",
                suggestion="Register the application in the Resource Registry.",
            )

        if not self._process_service.launch(app.executable):
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Unable to launch application.",
            )

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message="Application launched.",
            data={ "application": app.display_name, },
        )

    # ---------------------------------------------------------

    def _close(self, intent: Intent, ) -> ActionResult:

        app = self._registry.resolve_application(intent.target or "")

        if app is None:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Unknown application.",
            )

        if not self._process_service.terminate(app.process_name):
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Application is not running.",
            )

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message="Application closed.",
            data={ "application": app.display_name, },
        )

    # ---------------------------------------------------------

    def _running(self, intent: Intent,) -> ActionResult:

        app = self._registry.resolve_application(intent.target or "")

        if app is None:
            return ActionResult(
                status=ActionStatus.FAILED,
                message="Unknown application.",
            )

        running = self._process_service.is_running(app.process_name)

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message="Application state retrieved.",
            data={
                "application": app.display_name,
                "running": running,
            },
        )