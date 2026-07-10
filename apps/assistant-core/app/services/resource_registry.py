"""
resource_registry.py

Maintains mappings between user-friendly names and
desktop application metadata.

Every application has one canonical identifier while
supporting multiple aliases.

The registry is the single source of truth for
application metadata.
"""

from __future__ import annotations

from app.models.application_resource import ApplicationResource


class ResourceRegistry:

    def __init__(self) -> None:

        self._applications: dict[str, ApplicationResource] = {}
        self._alias_map: dict[str, str] = {}

        self._register(
            ApplicationResource(id="brave", display_name="Brave Browser",
                executable=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", process_name="brave.exe",
                aliases=("brave", "brave browser",),
            )
        )

        self._register(
            ApplicationResource(id="vscode", display_name="Visual Studio Code",
                executable=r"K:\Softwares\Microsoft VS Code\Code.exe", process_name="Code.exe",
                aliases=("visual studio code", "vs code", "vscode", "code",),
            )
        )

        self._register(
            ApplicationResource(id="spotify", display_name="Spotify",
                executable=r"C:\Users\RAINBOW\AppData\Local\Microsoft\WindowsApps\Spotify.exe", process_name="Spotify.exe",
                aliases=("spotify",),
            )
        )

    def _register(self, application: ApplicationResource,) -> None:

        self._applications[application.id] = application

        for alias in application.aliases:
            self._alias_map[alias.lower()] = application.id

    def resolve_application(self, name: str,) -> ApplicationResource | None:

        application_id = self._alias_map.get(name.lower())

        if application_id is None:
            return None

        return self._applications.get(application_id)

    def get_application(self, application_id: str,) -> ApplicationResource | None:

        return self._applications.get(application_id)
    
    @property
    def applications(self) -> tuple[ApplicationResource, ...]:
        """
        Returns every registered application.

        Exposed as an immutable tuple so callers can inspect the
        registry without modifying it.
        """
        return tuple(self._applications.values())