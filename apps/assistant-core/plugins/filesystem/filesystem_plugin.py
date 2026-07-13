"""
filesystem_plugin.py

Creates files and folders.

Filesystem path resolution is intentionally minimal in the MVP.
The LLM is expected to provide an absolute path or a well-known
folder until conversation and memory features are introduced.
"""

from __future__ import annotations

from pathlib import Path

from app.models.action_result import ActionResult
from app.models.action_result import ActionStatus
from app.models.capability import Capability
from app.models.intent import Intent
from app.models.plugin_metadata import PluginMetadata

from app.services.filesystem_service import FileSystemService

from plugins.base_plugin import BasePlugin


class FileSystemPlugin(BasePlugin):

    def __init__(self, filesystem: FileSystemService,) -> None:

        super().__init__(
            PluginMetadata(
                id="filesystem", name="Filesystem Plugin", version="1.0.0",
                author="CRASH-Owner", description="Creates filesystem resources.",
                capabilities=(
                    Capability(plugin="filesystem", action="create_folder", description="Create a folder",),
                    Capability(plugin="filesystem", action="create_file", description="Create a file",),
                ),
            )
        )

        self._filesystem = filesystem

    @property
    def metadata(self) -> PluginMetadata:
        return self._metadata

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def health_check(self) -> bool:
        return True

    def execute(self, intent: Intent,) -> ActionResult:

        match intent.action:

            case "create_folder":
                return self._create_folder(intent)

            case "create_file":
                print("Executing create_file action...")
                return self._create_file(intent)

            case _:
                return ActionResult(status=ActionStatus.FAILED, 
                    message=f"Unsupported filesystem action '{intent.action}'.",
                )

    # ---------------------------------------------------------

    def _create_folder(self, intent: Intent,) -> ActionResult:

        base_path = intent.target or ""
        folder_name = intent.parameters.get("name")

        if not folder_name:

            return ActionResult(status=ActionStatus.FAILED, 
                message="Folder name missing.",
            )

        full_path = str(Path(base_path) / folder_name)

        self._filesystem.create_folder(full_path)

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message="Folder created.",
            data={
                "path": full_path,
            },
        )

    # ---------------------------------------------------------

    def _create_file(self, intent: Intent,) -> ActionResult:

        base_path = intent.target or ""

        file_name = intent.parameters.get("name")

        if not file_name:

            return ActionResult(
                status=ActionStatus.FAILED,
                message="File name missing.",
            )

        full_path = str(
            Path(base_path) / file_name
        )

        self._filesystem.create_file(full_path)

        return ActionResult(
            status=ActionStatus.SUCCESS,
            message="File created.",
            data={
                "path": full_path,
            },
        )