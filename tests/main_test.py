from pathlib import Path
from unittest.mock import MagicMock, call, patch

from contactlookup.__main__ import _load_contacts_file
from contactlookup.definitions import (
    ROOT_DIR,
    SAMPLE_CONTACTS_DIR,
    SAMPLE_CONTACTS_FILE,
)
from contactlookup.services.file_data_store_service import FileDataStoreService
from contactlookup.utils import split_unix_path_string


@patch("contactlookup.__main__.logging.getLogger")
@patch("contactlookup.__main__.print")
def test_load_contacts_file_no_path(mock_print, mock_get_logger):
    # Mock the logger
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    # Mock the FileDataStoreService instance
    mock_service = MagicMock(spec=FileDataStoreService)

    # Call the function with no contacts file path
    _load_contacts_file(mock_service, None)

    # Check if the print statements were called
    mock_print.assert_has_calls(
        [call("No contacts file provided."), call("Using default contacts file: None")],
    )

    # Check if the logger info was called
    mock_logger.info.assert_has_calls(
        [
            call("No contacts file provided. Using default contacts file."),
            call("Application is in development mode."),
        ],
    )

    # Check if the contacts file was set to the default path
    sample_contacts_dir_parts = split_unix_path_string(SAMPLE_CONTACTS_DIR)
    base_path = ROOT_DIR.parent
    base_path = base_path / Path("/".join(sample_contacts_dir_parts))
    development_contacts_file_path = base_path / SAMPLE_CONTACTS_FILE
    expected_path = development_contacts_file_path
    mock_service.set_contacts_file_path.assert_called_once_with(expected_path)


@patch("contactlookup.__main__.logging.getLogger")
@patch("contactlookup.__main__.print")
def test_load_contacts_file_with_path(mock_print, mock_get_logger):
    # Mock the logger
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    # Mock the FileDataStoreService instance
    mock_service = MagicMock(spec=FileDataStoreService)

    # Define a valid contacts file path
    # Use an actual path to a contacts file in the system:
    # Will use $HOME/contacts.vcf
    # For Windows, use the path-to-string conversion approach
    contacts_file_path = Path.home() / "contacts.vcf"
    contacts_file_path_str = str(contacts_file_path)

    # Call the function with a valid contacts file path
    _load_contacts_file(mock_service, contacts_file_path_str)

    # Check if the print statement was not called
    mock_print.assert_not_called()

    # # Check if the logger info was called
    mock_logger.info.assert_called_once_with(
        "Using contacts file: %s",
        contacts_file_path_str,
    )

    # # Check if the contacts file was set to the provided path
    expected_path = Path(contacts_file_path)
    mock_service.set_contacts_file_path.assert_called_once_with(expected_path)
