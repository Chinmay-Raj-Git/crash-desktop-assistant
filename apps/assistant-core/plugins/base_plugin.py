"""
base_plugin.py

Base implementation shared by all plugins.
"""

from abc import ABC
import json
from pathlib import Path

from app.interfaces.plugin import IPlugin
from app.models.intent import Intent
from app.models.plugin_metadata import PluginMetadata
from app.exceptions import UnsupportedCapabilityError


class BasePlugin(IPlugin, ABC):
    """
    Base implementation for plugins.
    Provides common validation and default lifecycle methods.
    """

    def __init__(self, metadata: PluginMetadata) -> None:
        self._metadata = metadata

    @property
    def metadata(self) -> PluginMetadata:
        return self._metadata

    def initialize(self) -> None:
        """
        Default initialization.
        Override only if needed.
        """
        pass

    def shutdown(self) -> None:
        """
        Default cleanup.
        Override only if needed.
        """
        pass

    def health_check(self) -> bool:
        return True

    def validate_intent(self, intent: Intent) -> None:
        """
        Ensures this plugin supports the requested capability.
        """

        if intent.capability not in self.metadata.capability_ids:
            raise UnsupportedCapabilityError(
                f"{self.metadata.name} does not support "
                f"'{intent.capability}'."
            )
            
    @staticmethod            
    def _load_metadata(path: Path, capabilities,) -> PluginMetadata:

        with path.open(encoding="utf-8",) as file:
            data = json.load(file)

        return PluginMetadata(id=data["id"], name=data["name"], version=data["version"],
            author=data["author"], description=data["description"], capabilities=capabilities,
        )