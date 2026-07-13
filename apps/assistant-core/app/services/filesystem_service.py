"""
filesystem_service.py

Provides filesystem operations for plugins.

This service isolates all direct interaction with the
operating system.
"""

from __future__ import annotations

import os
from pathlib import Path


class FileSystemService:
    # ---------------------------------------------------------

    def create_folder(self, path: str,) -> bool:

        Path(path).mkdir(parents=True, exist_ok=True,)

        return True

    # ---------------------------------------------------------

    def create_file(self, path: str,) -> bool:

        Path(path).touch(exist_ok=True,)

        return True