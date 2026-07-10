"""
config_loader.py

Loads configuration from disk and maps it
onto the Settings model.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.config.settings import Settings


class ConfigLoader:
    """
    Loads application configuration.
    """

    def __init__(self, settings: Settings,) -> None:

        self.settings = settings

    def load(self) -> Settings:
        """
        Loads configuration if present.

        Missing values fall back
        to defaults defined in Settings.
        """

        config_path = self.settings.config_file

        if not config_path.exists():
            return self.settings

        with open(config_path, "r", encoding="utf-8",) as file:
            config = json.load(file)

        for key, value in config.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value,)

        return self.settings

    def save(self) -> None:
        """
        Persists settings to disk.
        """

        self.settings.config_file.parent.mkdir(parents=True, exist_ok=True,)

        from dataclasses import asdict

        data = asdict(self.settings)

        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)

        with open(
            self.settings.config_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )