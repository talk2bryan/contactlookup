# Project Root Folder
from pathlib import Path

ROOT_DIR = Path(__file__).parents[0]
LOGGING_CONFIG_PATH = ROOT_DIR / "logging_configuration.conf"
APP_LOG_FILENAME = "contactlookup.log"

# Constants
VCF_EXTENSION = ".vcf"
SAMPLE_CONTACTS_DIR = "tests/data"
SAMPLE_CONTACTS_FILE = "contactlookup_sample_contacts.vcf"
FILE_DATA_STORE_SERVICE = "f"

# Server settings, overridable with environment variables
API_KEY_ENV_VAR = "CONTACTLOOKUP_API_KEY"
API_KEY_HEADER = "X-API-Key"
HOST_ENV_VAR = "CONTACTLOOKUP_HOST"
PORT_ENV_VAR = "CONTACTLOOKUP_PORT"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
