# Initialize logger
import logging.config
from pathlib import Path

from contactlookup.definitions import LOGGING_CONFIG_PATH

# homepath = $HOME
HOMEPATH = str(Path.home())
logging.config.fileConfig(
    fname=LOGGING_CONFIG_PATH,
    disable_existing_loggers=False,
    defaults={"log_dir": HOMEPATH},
)
logger = logging.getLogger(__name__)
logger.info("Logger initialized")
