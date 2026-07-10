"""
plugin.py

Defines the base interface for every plugin.

Every plugin in the assistant must inherit from IPlugin.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.action_result import ActionResult
from app.models.intent import Intent
from app.models.plugin_metadata import PluginMetadata


class IPlugin(ABC):
    """
    Base contract implemented by every plugin.
    """

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """
        Returns immutable plugin metadata.
        """
        raise NotImplementedError

    @abstractmethod
    def initialize(self) -> None:
        """
        Called once during assistant startup.

        Use this for loading configuration,
        checking dependencies,
        or preparing resources.
        """
        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> None:
        """
        Called before the assistant exits.

        Plugins should release resources here.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, intent: Intent) -> ActionResult:
        """
        Executes a validated intent.

        Returns an ActionResult describing the outcome.
        """
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> bool:
        """
        Returns whether the plugin is healthy.

        Used during startup and diagnostics.
        """
        raise NotImplementedError