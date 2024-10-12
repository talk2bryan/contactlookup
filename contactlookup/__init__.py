"""Initialize logger"""

import logging.config
from pathlib import Path

from contactlookup.definitions import APP_LOG_FILENAME, LOGGING_CONFIG_PATH

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
