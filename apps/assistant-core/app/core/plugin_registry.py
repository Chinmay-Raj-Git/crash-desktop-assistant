"""
plugin_registry.py

Stores every loaded plugin and every registered capability.

The registry is the single source of truth for:

- Available plugins
- Available capabilities

The dispatcher queries this registry to determine which plugin
should execute an incoming intent.
"""

from app.interfaces.plugin import IPlugin
from app.models.capability import Capability


class PluginRegistry:
    """
    Central registry for plugins and capabilities.
    """

    def __init__(self) -> None:
        self._plugins: dict[str, IPlugin] = {}
        self._capabilities: dict[str, Capability] = {}

    def register(self, plugin: IPlugin) -> None:
        """
        Registers a plugin and all of its capabilities.
        """

        plugin_id = plugin.metadata.id

        if plugin_id in self._plugins:
            raise ValueError(
                f"Plugin '{plugin_id}' is already registered."
            )

        self._plugins[plugin_id] = plugin

        for capability in plugin.metadata.capabilities:

            if capability.id in self._capabilities:
                raise ValueError(
                    f"Capability '{capability.id}' "
                    "already registered."
                )

            self._capabilities[capability.id] = capability

    def get_plugin(self, plugin_id: str) -> IPlugin:
        """
        Returns a plugin by ID.
        """
        return self._plugins[plugin_id]

    def get_plugin_for_capability(
        self,
        capability_id: str,
    ) -> IPlugin:
        """
        Returns the plugin responsible for a capability.
        """
        return self._plugins[self._capabilities[capability_id].plugin]

    def has_capability(self, capability_id: str) -> bool:
        """
        Checks if a capability exists.
        """
        return capability_id in self._capabilities
    
    def get_capability(self, capability_id: str) -> Capability:
        """
        Returns a capability by ID.
        """
        if self.has_capability(capability_id) is False:
            raise ValueError(f"Capability '{capability_id}' not found.")
        
        return self._capabilities[capability_id]

    @property
    def plugins(self) -> tuple[IPlugin, ...]:
        """
        Returns all registered plugins.
        """
        return tuple(self._plugins.values())

    @property
    def capabilities(self) -> tuple[str, ...]:
        """
        Returns every registered capability.
        """
        return tuple(sorted(self._capabilities.keys()))