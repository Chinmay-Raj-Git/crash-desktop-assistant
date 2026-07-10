"""
application_resource.py

Immutable representation of an installed desktop application.

This model is returned by the ResourceRegistry and contains
everything required to interact with an application.

The registry is the single source of truth for application metadata.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ApplicationResource:
    """
    Represents one desktop application.

    Attributes
    ----------
    id:
        Canonical identifier used internally.

    display_name:
        Human-friendly application name.

    executable:
        Full executable path used for launching.

    process_name:
        Executable filename used when checking
        running processes or terminating them.

    aliases:
        Accepted user-facing names.
    """

    id: str

    display_name: str

    executable: str

    process_name: str

    aliases: tuple[str, ...]