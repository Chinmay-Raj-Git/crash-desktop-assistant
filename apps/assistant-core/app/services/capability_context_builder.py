"""
capability_context_builder.py

Builds the assistant capability context that is supplied to
an LLM during intent parsing.

The builder is intentionally independent of any specific LLM.
"""

from __future__ import annotations

from app.core.plugin_registry import PluginRegistry
from app.services.resource_registry import ResourceRegistry


class CapabilityContextBuilder:

    def __init__(self, plugin_registry: PluginRegistry, resource_registry: ResourceRegistry,) -> None:

        self._plugin_registry = plugin_registry
        self._resource_registry = resource_registry

    def build(self) -> str:
        """
        Builds a textual description of the assistant's
        current capabilities.

        This text will later become part of the system prompt
        for cloud LLM providers.
        """

        lines: list[str] = []

        lines.append("Available plugins and capabilities:\n")

        for plugin in self._plugin_registry.plugins:

            lines.append(f"- {plugin.metadata.id}")

            for capability in plugin.metadata.capabilities:
                lines.append(f"    - {capability.action}")

        lines.append("")
        lines.append("Known desktop applications:\n")

        for app in self._resource_registry.applications:

            aliases = ", ".join(app.aliases)

            lines.append(
                f"- {app.display_name} "
                f"(aliases: {aliases})"
            )

        return "\n".join(lines)