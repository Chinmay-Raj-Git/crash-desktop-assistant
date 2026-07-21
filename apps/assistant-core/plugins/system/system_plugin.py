"""
system_plugin.py

Provides system-wide operating system commands.
"""

from __future__ import annotations

from pathlib import Path

from app.models.action_result import ActionResult
from app.models.action_result import ActionStatus
from app.models.capability import Capability
from app.models.intent import Intent

from app.services.system_service import SystemService

from plugins.base_plugin import BasePlugin


class SystemPlugin(BasePlugin):

    def __init__(self, system: SystemService, ) -> None:

        metadata = self._load_metadata(
            Path(__file__).parent / "plugin.json",
            capabilities=(
                Capability(
                    plugin="system",
                    action="lock",
                    description="Lock the computer",
                    confirmation_message = "Woah there dude! watch out, imma lock your pc fr...",
                    requires_confirmation = True
                ),
                Capability(
                    plugin="system",
                    action="sleep",
                    description="Put the computer to sleep",
                    confirmation_message = "Woah there dude! watch out, imma sleep your pc fr...",
                    requires_confirmation = True
                ),
                Capability(
                    plugin="system",
                    action="shutdown",
                    description="Shutdown the computer",
                    confirmation_message = "Woah there dude! watch out, imma shut your pc fr...",
                    requires_confirmation = True
                ),
                Capability(
                    plugin="system",
                    action="restart",
                    description="Restart the computer",
                    confirmation_message = "Woah there dude! watch out, imma restart your pc fr...",
                    requires_confirmation = True
                ),
            ),
        )

        super().__init__(metadata)

        self._system = system

    def execute(
        self,
        intent: Intent,
    ) -> ActionResult:

        match intent.action:

            case "lock":
                success = self._system.lock()

            case "sleep":
                success = self._system.sleep()

            case "shutdown":
                success = self._system.shutdown()

            case "restart":
                success = self._system.restart()

            case _:
                return ActionResult(
                    status=ActionStatus.FAILED,
                    message="Unsupported system action.",
                )

        if success:

            return ActionResult(
                status=ActionStatus.SUCCESS,
                message="System command executed.",
            )

        return ActionResult(
            status=ActionStatus.FAILED,
            message="Unable to execute system command.",
        )