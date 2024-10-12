from contactlookup.utils import split_unix_path_string


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
