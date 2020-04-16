from contextlib import nullcontext as does_not_raise
from io import StringIO

import pytest
from munch import munchify

from victoria.storage import azure_provider


@pytest.fixture
def mock_azure_classes(monkeypatch):
    class BlockBlobServiceMock:
        def __init__(self, **kwargs):
            self.blobs = {}

        def create_blob_from_stream(self, container, key, data):
            self.blobs[key] = data.read()

        def create_blob_from_text(self, container, key, data):
            self.blobs[key] = data

        def create_blob_from_bytes(self, container, key, data):
            self.blobs[key] = data

        def get_blob_to_stream(self, container, key, stream):
            stream.write(self.blobs[key])
            return stream

        def list_blobs(self, container):
            for key, _ in self.blobs.items():
                yield munchify({"name": key})

    monkeypatch.setattr(azure_provider, "BlockBlobService",
                        BlockBlobServiceMock)


@pytest.mark.parametrize(
    "data,key,expected,raises",
    [("test", "text_blob.txt", "test", does_not_raise()),
     (b"test", "byte_blob.bin", b"test", does_not_raise()),
     (StringIO("test"), "stream_blob.txt", "test", does_not_raise()),
     (123, "invalid_blob", None, pytest.raises(TypeError))])
def test_store(mock_azure_classes, data, key, expected, raises):
    with raises:
        provider = azure_provider.AzureStorageProvider("", "", "container")
        provider.store(data, key)
        assert provider.client.blobs[key] == expected


def test_retrieve(mock_azure_classes):
    provider = azure_provider.AzureStorageProvider("", "", "container")
    provider.store("test", "test.file")
    stream = StringIO()
    provider.retrieve("test.file", stream)
    assert stream.getvalue() == "test"


def test_ls(mock_azure_classes):
    provider = azure_provider.AzureStorageProvider("", "", "container")
    provider.store("test", "test.file")
    provider.store("test", "test2.file")
    ls = list(provider.ls())
    assert ls == ["test.file", "test2.file"]


def test_ensure_container(mock_azure_classes):
    provider = azure_provider.AzureStorageProvider("", "", "")
    with pytest.raises(ValueError):
        provider._ensure_container()