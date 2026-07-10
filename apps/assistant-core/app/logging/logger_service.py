"""
logger_service.py

Concrete implementation of ILogger.
"""

from pathlib import Path
import logging

from app.interfaces.logger import ILogger


class LoggerService(ILogger):
    """
    Default logger implementation.
    """

    def __init__(self, log_directory: Path) -> None:

        log_directory.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger("assistant")

        if self._logger.handlers:
            return

        self._logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s : %(message)s"
        )

        file_handler = logging.FileHandler(
            log_directory / "assistant.log",
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    def debug(self, message: str, **context) -> None:
        self._logger.debug(self._format(message, context))

    def info(self, message: str, **context) -> None:
        self._logger.info(self._format(message, context))

    def warning(self, message: str, **context) -> None:
        self._logger.warning(self._format(message, context))

    def error(self, message: str, **context) -> None:
        self._logger.error(self._format(message, context))

    def critical(self, message: str, **context) -> None:
        self._logger.critical(self._format(message, context))

    @staticmethod
    def _format(message: str, context: dict) -> str:

        if not context:
            return message

        details = ", ".join(
            f"{key}={value}"
            for key, value in context.items()
        )

        return f"{message} | {details}"