"""Main module for the contactlookup package."""

import logging
import site
import traceback
from pathlib import Path

import fire
import uvicorn

import contactlookup.controller as app_controller
from contactlookup.definitions import (
    FILE_DATA_STORE_SERVICE,
    ROOT_DIR,
    SAMPLE_CONTACTS_DIR,
    SAMPLE_CONTACTS_FILE,
)
from contactlookup.services.data_store_service import DataStoreService
from contactlookup.services.file_data_store_service import FileDataStoreService
from contactlookup.utils import split_unix_path_string


def _load_contacts_file(service: FileDataStoreService, contacts_file_path: str | None):
    # Ensure the contacts file path is provided.
    # If no file is provided by the user, use the default contacts file:
    # SAMPLE_CONTACTS_DIR/SAMPLE_CONTACTS_FILE in the tests directory.
    logger = logging.getLogger(__name__)
    contacts_file: Path | None = None
    if not contacts_file_path:
        print("No contacts file provided.")
        logger.info("No contacts file provided. Using default contacts file.")
        # The data directory is in the tests directory which is installed in
        # the site-packages directory.

        try:
            # First check for tests/data/contacts.vcf in root's directory.
            # If we are developing the package, the contacts file will be in
            # ROOT_DIR/../tests/data/contacts.vcf
            base_path = ROOT_DIR.parent

            # To support Windows, we need to split the Unix path string into a
            # list of path components.
            sample_contacts_dir_parts = split_unix_path_string(SAMPLE_CONTACTS_DIR)
            base_path = base_path / Path("/".join(sample_contacts_dir_parts))
            development_contacts_file_path = base_path / SAMPLE_CONTACTS_FILE

            if development_contacts_file_path.exists():
                contacts_file = development_contacts_file_path
                logger.info("Application is in development mode.")
            else:
                # We are not developing the package. The contacts file will be
                # in the site-packages directory.
                # Check for tests/data/contacts.vcf in the site-packages directory
                site_packages_dir = Path(site.getsitepackages()[0])
                base_path = site_packages_dir / Path(
                    "/".join(sample_contacts_dir_parts),
                )
                contacts_file = base_path / SAMPLE_CONTACTS_FILE
                logger.info("Application is in production mode.")
            print(f"Using default contacts file: {contacts_file_path}")
        except ImportError as e:
            print(
                "Could not find site-packages directory. Please provide a contacts file.",
            )
            stack_trace = traceback.format_exc()
            logger.error(
                "_load_contacts_file|Error loading contacts file: %s. Exiting",
                e,
            )
            logger.error("_load_contacts_file|Stack trace: %s", stack_trace)
            return
    else:
        # If the user provides a contacts file, use it.
        contacts_file = Path(contacts_file_path.strip())
        logger.info("Using contacts file: %s", contacts_file_path)

    service.set_contacts_file_path(contacts_file)


def _setup(
    data_store_service: str | None = None,
    contacts_file_path: str | None = None,
) -> DataStoreService | None:
    """
    data_store_service is used to indicate the type of data store service to
    use.
    Options:
    1. f: indicates FileDataStoreService
    2. d: indicates DatabaseDataStoreService (not implemented)

    If no data_store_service is provided, the default is FileDataStoreService.
    If an invalid data_store_service is provided, the default is FileDataStoreService.
    """
    logger = logging.getLogger(__name__)
    if not data_store_service:
        data_store_service = FILE_DATA_STORE_SERVICE
    data_store_service = data_store_service.strip().lower()

    logger.info("Using data store service option: %s", data_store_service)
    # Tell the user what data store service is being used
    if data_store_service == FILE_DATA_STORE_SERVICE:
        print("Using FileDataStoreService")
    else:
        # Not implemented databaseconnection. Would require a database connection.
        print("Invalid data store service. Using FileDataStoreService")
        print(f"data_store_service: {data_store_service}")
        data_store_service = FILE_DATA_STORE_SERVICE

    service = FileDataStoreService()
    _load_contacts_file(service=service, contacts_file_path=contacts_file_path)
    initialized = service.initialize()
    if not initialized:
        logger.error("Data store service failed to initialize")
        print("Data store service failed to initialize")
        return None
    return service


def cli():
    """Command line interface."""
    fire.Fire(main)


def main(service: str | None = FILE_DATA_STORE_SERVICE, file: str | None = None):
    """Expose API to query contacts.

    Args:
        service (str | None, optional): The data store service to use. Defaults to FILE_DATA_STORE_SERVICE.
        file (str | None, optional): The path to the contacts file. Defaults to None.
    """
    data_store_service = _setup(data_store_service=service, contacts_file_path=file)
    if not data_store_service:
        return

    # At this point, the data store service is initialized
    # We can now run the FastAPI application
    logger = logging.getLogger(__name__)
    logger.info("Data store service initialized")
    print("Data store service initialized")

    app_controller.set_data_store_service(data_store_service)

    # Run the FastAPI application
    try:
        logger.info("Starting FastAPI application")
        uvicorn.run(app_controller.app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error("Error starting FastAPI application: %s", e)
        print(f"Error starting FastAPI application: {e}")
        stack_trace = traceback.format_exc()
        logger.error("Stack trace: %s", stack_trace)


if __name__ == "__main__":
    fire.Fire(main)
