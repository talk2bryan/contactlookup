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
