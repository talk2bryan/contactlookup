import logging

from contactlookup.utils import initialize_application_logger, split_unix_path_string


def test_split_unix_path_string():
    # Test with a simple Unix path
    path = "/home/user/docs"
    expected = ["", "home", "user", "docs"]
    assert split_unix_path_string(path) == expected

    # Test with a root path
    path = "/"
    expected = ["", ""]
    assert split_unix_path_string(path) == expected

    # Test with an empty path
    path = ""
    expected = [""]
    assert split_unix_path_string(path) == expected

    # Test with a path that has trailing slashes
    path = "/home/user/docs/"
    expected = ["", "home", "user", "docs", ""]
    assert split_unix_path_string(path) == expected

    # Test with a path that has multiple slashes
    path = "/home//user/docs"
    expected = ["", "home", "", "user", "docs"]
    assert split_unix_path_string(path) == expected

    # Test with a path that has no leading slash
    path = "home/user/docs"
    expected = ["home", "user", "docs"]
    assert split_unix_path_string(path) == expected


def test_initialize_application_logger():
    # Call the function to initialize the logger
    initialize_application_logger()

    # Get the logger instance
    logger = logging.getLogger()

    # Check if the logger has handlers
    assert len(logger.handlers) > 0

    # Check if the logger level is set correctly
    assert logger.level == logging.DEBUG

    # Check if the first handler is a TimedRotatingFileHandler
    assert isinstance(logger.handlers[0], logging.FileHandler)

    # Check if the handler is a TimedRotatingFileHandler
    assert isinstance(logger.handlers[0], logging.handlers.TimedRotatingFileHandler)

    # Check if the formatter is set correctly (assuming a specific format)
    expected_format = (
        "%(asctime)s - %(name)s (%(filename)s:%(lineno)d): [%(levelname)s] %(message)s"
    )
    assert logger.handlers[0].formatter._fmt == expected_format
