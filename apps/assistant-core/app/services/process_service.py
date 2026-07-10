from __future__ import annotations

import subprocess
import psutil
from pathlib import Path


class ProcessService:
    """
    Handles process-related operations.

    This service isolates OS-specific behaviour from plugins.
    """

    def launch(self, executable: str) -> bool:
        try:
            subprocess.Popen([executable])
            return True
        except Exception:
            return False

    def terminate(self, process_name: str) -> bool:
        terminated = False

        for process in psutil.process_iter(["name"]):
            try:
                if process.info["name"] and process.info["name"].lower() == process_name.lower():
                    process.kill()
                    terminated = True
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

        return terminated

    def is_running(self, process_name: str) -> bool:
        for process in psutil.process_iter(["name"]):
            try:
                if process.info["name"] and process.info["name"].lower() == process_name.lower():
                    return True
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

        return False