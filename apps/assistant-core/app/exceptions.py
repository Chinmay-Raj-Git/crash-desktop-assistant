"""
exceptions.py

Custom exceptions used throughout the assistant.

Using project-specific exceptions makes debugging easier
and avoids relying on generic Python exceptions.
"""


class AssistantError(Exception):
    """Base exception for all assistant-related errors."""


class PluginError(AssistantError):
    """Base exception for plugin-related errors."""


class PluginAlreadyRegisteredError(PluginError):
    """Raised when attempting to register a duplicate plugin."""


class PluginNotFoundError(PluginError):
    """Raised when a requested plugin cannot be found."""


class UnknownCapabilityError(PluginError):
    """Raised when no plugin supports a requested capability."""


class UnsupportedCapabilityError(PluginError):
    """Raised when a plugin receives an unsupported capability."""


class ConfigurationError(AssistantError):
    """Raised when configuration cannot be loaded or is invalid."""


class ServiceNotFoundError(AssistantError):
    """Raised when a service cannot be resolved from the container."""