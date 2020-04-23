from contextlib import nullcontext as does_not_raise
from io import StringIO, BytesIO
from os import path

import pytest
from pyfakefs.pytest_plugin import fs

from victoria.storage import local_provider


@pytest.mark.parametrize(
    "data,key,expected,raises",
    [("test", "text_blob.txt", "test", does_not_raise()),
     (b"test", "byte_blob.bin", b"test", does_not_raise()),
     (StringIO("test"), "stream_blob.txt", "test", does_not_raise()),
     (123, "invalid_blob", None, pytest.raises(TypeError))])
def test_store(fs, data, key, expected, raises):
    with raises:
        provider = local_provider.LocalStorageProvider("container")
        provider.store(data, key)
        assert path.exists(path.join("container", key)) == True


def test_retrieve(fs):
    provider = local_provider.LocalStorageProvider("container")
    provider.store(b"test", "test.file")
    stream = BytesIO()
    provider.retrieve("test.file", stream)
    assert stream.getvalue() == b"test"


def test_ls(fs):
    provider = local_provider.LocalStorageProvider("container")
    provider.store("test", "test.file")
    provider.store("test", "test2.file")
    ls = list(provider.ls())
    assert ls == [
        path.join("container", "test.file"),
        path.join("container", "test2.file")
    ]


def test_ensure_container(fs):
    provider = local_provider.LocalStorageProvider("container")
    assert path.exists("container") == False
    provider._ensure_container()
    assert path.exists("container") == True
