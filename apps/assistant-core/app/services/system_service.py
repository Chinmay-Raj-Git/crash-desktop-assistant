"""
system_service.py

Provides operating system level functionality used by
SystemPlugin.

All interaction with Windows is isolated here.
"""

from __future__ import annotations

import ctypes
import os


class SystemService:

    def lock(self) -> bool:

        return bool(ctypes.windll.user32.LockWorkStation())

    # ---------------------------------------------------------

    def sleep(self) -> bool:

        return os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0") == 0

    # ---------------------------------------------------------

    def shutdown(self) -> bool:

        return os.system("shutdown /s /t 0") == 0

    # ---------------------------------------------------------

    def restart(self) -> bool:

        return os.system("shutdown /r /t 0") == 0