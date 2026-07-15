"""
plugin_manager.py

Responsible for the lifecycle of every plugin.

Responsibilities:

- Loading plugins
- Initializing plugins
- Health checking
- Registration
- Shutdown
"""

from __future__ import annotations

from app.core.plugin_registry import PluginRegistry
from app.interfaces.logger import ILogger
from app.interfaces.plugin import IPlugin

from plugins.application.application_plugin import ApplicationPlugin
from plugins.browser.browser_plugin import BrowserPlugin
from plugins.filesystem.filesystem_plugin import FileSystemPlugin
from plugins.system.system_plugin import SystemPlugin


class PluginManager:
    """
    Handles plugin lifecycle.
    """

    def __init__(self, registry: PluginRegistry, logger: ILogger,) -> None:

        self._registry = registry
        self._logger = logger

        self._plugins: list[IPlugin] = []

    def load_plugin(self, plugin: IPlugin, ) -> None:
        """
        Loads a single plugin.
        """

        self._logger.info(
            "Loading plugin",
            plugin=plugin.metadata.name,
        )

        plugin.initialize()

        if not plugin.health_check():

            raise RuntimeError(
                f"{plugin.metadata.name} failed health check."
            )

        self._registry.register(plugin)

        self._plugins.append(plugin)

        self._logger.info(
            "Plugin loaded",
            plugin=plugin.metadata.name,
        )
        
    def load_all(self, *, resource_registry, process_service, filesystem_service, system_service) -> None:
        
        self.load_plugin(ApplicationPlugin(registry=resource_registry, process_service=process_service))

        self.load_plugin(BrowserPlugin())

        self.load_plugin(SystemPlugin(system=system_service))

        self.load_plugin(FileSystemPlugin(filesystem=filesystem_service))

    def shutdown(self) -> None:
        """
        Gracefully shuts down every plugin.
        """

        for plugin in reversed(self._plugins):

            self._logger.info(
                "Shutting down plugin",
                plugin=plugin.metadata.name,
            )

            plugin.shutdown()