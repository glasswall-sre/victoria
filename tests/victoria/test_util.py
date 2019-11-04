import pytest

import victoria.util


@pytest.mark.parametrize("path,expected", [("test.py", "test"),
                                           ("/in/a/directory/test.py", "test"),
                                           ("in/a/directory/test.py", "test"),
                                           ("test/", ""),
                                           ("in/a/directory/test/", ""),
                                           ("/in/a/directory/test/", "")])
def test_basenamenoext(path, expected):
    result = victoria.util.basenamenoext(path)
    assert result == expected