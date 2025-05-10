"""Logger and other default settings for the Delos client."""

from enum import Enum

from loguru import logger as delos_logger


class VerboseLevel(int, Enum):
    """Verbose level for the logger."""

    NONE = 0
    INFO = 1
    DEBUG = 2


__all__ = ["VerboseLevel", "delos_logger"]
