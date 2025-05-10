# Future Library
from __future__ import annotations

# Standard Library
import logging

from dataclasses import field
from typing import Optional

# 3rd Party Library
from pydantic.dataclasses import dataclass

# 1st Party Library
from rwskit.cli import LogLevel
from rwskit.config import YamlConfig

log = logging.getLogger(__name__)

DEFAULT_LOGGING_LEVEL: str = "INFO"
DEFAULT_LOGGING_FORMAT: str = (
    "%(asctime)-15s [%(name)s]:%(lineno)d %(levelname)s %(message)s"
)


@dataclass(kw_only=True, frozen=True, config={"arbitrary_types_allowed": True})
class LoggingConfig(YamlConfig):
    """Logging configuration."""

    level: LogLevel = LogLevel(DEFAULT_LOGGING_LEVEL)
    """The logging level."""

    format: str = DEFAULT_LOGGING_FORMAT
    """The logging format"""

    filename: Optional[str] = None
    """Log to this file instead of stderr."""

    log_level_overrides: dict[str, LogLevel | int] = field(default_factory=dict)
    """Override the log level for specific named loggers."""

    @property
    def is_logging_configured(self) -> bool:
        """Tries to determine if logging has already been configured.

        This method simply checks if any handlers are present. The existence
        of at least one handler indicates it is likely that some library
        (including our own) has already configured logging.

        Returns
        -------
        bool
            ``True`` if logging is already configured.
        """
        return bool(logging.getLogger().handlers)

    def configure(self):
        if self.is_logging_configured:
            log.warning(
                "Unable to configure logging because it has likely already been "
                "configured."
            )
        else:
            logging.basicConfig(
                filename=self.filename, level=self.level, format=self.format
            )

        for log_name, log_level in self.log_level_overrides.items():
            log.debug(f"Overriding logger '{log_name}' with level '{log_level}'")
            logging.getLogger(log_name).setLevel(log_level)
