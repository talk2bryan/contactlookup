"""Utility functions for the Contact Lookup application."""

import logging.config
from pathlib import Path

from contactlookup.definitions import APP_LOG_FILENAME, LOGGING_CONFIG_PATH


def split_unix_path_string(path_string: str) -> list[str]:
    """Breaks a Unix path string into a list of path components.

    This is to enable the use of Unix path strings in Windows environments. The
    output list can be used to construct a Windows path string.

    Args:
        path_string (str): A Unix path string.

    Returns:
        list[str]: A list of path components.
    """
    return path_string.split("/")


def initialize_application_logger():
    """Initializes the application logger."""
    # If an /app directory is not present, we use $HOME as the log directory.
    # If an /app directory is present, we use /app as the log directory.
    _default_log_dir = Path("/app")
    if _default_log_dir.exists():
        LOG_DIR = _default_log_dir
    else:
        LOG_DIR = Path.home()

    # Convert the log_file_path to raw string for Windows compatibility.
    log_file_str = str(LOG_DIR / APP_LOG_FILENAME).replace("\\", "\\\\")

    logging.config.fileConfig(
        fname=LOGGING_CONFIG_PATH,
        disable_existing_loggers=False,
        defaults={"log_file": log_file_str},
    )
    logger = logging.getLogger(__name__)
    logger.info("Logger initialized")
