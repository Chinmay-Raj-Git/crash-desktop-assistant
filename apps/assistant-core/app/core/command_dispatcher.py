"""
command_dispatcher.py

Routes validated intents to the appropriate plugin.
"""

from __future__ import annotations

from app.core.plugin_registry import PluginRegistry
from app.models.action_result import ActionResult
from app.models.action_result import ActionStatus
from app.models.intent import Intent


class CommandDispatcher:

    def __init__(self, registry: PluginRegistry, ) -> None:
        
        self._registry = registry

    def dispatch(self, intent: Intent, *, skip_confirmation: bool = False,) -> ActionResult:

        if not self._registry.has_capability(intent.capability):

            return ActionResult(
                status=ActionStatus.FAILED,
                message="Unknown capability.",
                error=intent.capability,
            )
            
        intent.requires_confirmation = self._registry.get_capability(intent.capability).requires_confirmation
            
        if intent.requires_confirmation and not skip_confirmation:
            return ActionResult(
                status=ActionStatus.UNCONFIRMED,
                message=intent.confirmation_message or "Are you sure you want to proceed?",
                error=intent.capability,
            )

        plugin = self._registry.get_plugin_for_capability(intent.capability)

        return plugin.execute(intent)