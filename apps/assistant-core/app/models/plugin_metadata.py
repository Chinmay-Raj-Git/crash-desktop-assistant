"""
plugin_metadata.py

Defines metadata describing a plugin.

The Plugin Manager uses this information during discovery,
registration, logging, and health checks.
"""

from dataclasses import dataclass, field

from app.models.capability import Capability


@dataclass(slots=True, frozen=True)
class PluginMetadata:
    """
    Immutable metadata describing a plugin.
    """

    # Unique plugin identifier
    id: str

    # Human-readable name
    name: str

    # Semantic version
    version: str

    # Plugin author
    author: str

    # Short description
    description: str

    # Capabilities exposed by this plugin
    capabilities: tuple[Capability, ...] = field(default_factory=tuple)

    # Can the plugin be disabled?
    enabled: bool = True

    @property
    def capability_ids(self) -> tuple[str, ...]:
        """
        Returns all capability IDs.

        Example:
        (
            "application.launch",
            "application.close"
        )
        """
        return tuple(capability.id for capability in self.capabilities)