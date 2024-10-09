# Project Root Folder
from pathlib import Path

ROOT_DIR = Path(__file__).parents[0]
LOGGING_CONFIG_PATH = ROOT_DIR / "logging_configuration.conf"


# Constants
VCF_EXTENSION = ".vcf"
SAMPLE_CONTACTS_DIR = "tests/data"
SAMPLE_CONTACTS_FILE = "contacts.vcf"
