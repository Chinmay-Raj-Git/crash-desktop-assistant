"""
plugin_health.py
"""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PluginHealth:

    healthy: bool

    message: str = "OK"