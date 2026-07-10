"""
settings.py

Defines strongly-typed application settings.

All default configuration values live here.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    """
    Application settings.
    """

    assistant_name: str = "CRASH"

    version: str = "0.1.0"

    log_directory: Path = Path("logs")

    plugins_directory: Path = Path("plugins")

    config_file: Path = Path("config/config.json")

    default_personality: str = (
        "Professional"
    )

    llm_provider: str = "mock"

    debug: bool = False