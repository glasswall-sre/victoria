from contextlib import nullcontext as does_not_raise
from io import IOBase, StringIO, RawIOBase

import pytest
from munch import munchify

from victoria.storage import azure_provider


@pytest.fixture
def mock_azure_classes(monkeypatch):
    class MockStreamDownloader(RawIOBase):
        def __init__(self, contents):
            self.stream = StringIO(contents)

        def readall(self):
            return self.stream.read()

    class BlobClientMock:
        def __init__(self):
            self.data = None

        def upload_blob(self, data):
            if isinstance(data, IOBase):
                self.data = data.read()
            else:
                self.data = data

        def download_blob(self):
            return MockStreamDownloader(self.data)

    class BlobServiceClientMock:
        @classmethod
        def from_connection_string(cls, conn_str: str):
            return cls()

        def get_container_client(self, container: str):
            return ContainerClientMock()

    class ContainerClientMock:
        def __init__(self, *args, **kwargs):
            self.blobs = {}

        def list_blobs(self):
            for key, _ in self.blobs.items():
                yield munchify({"name": key})

        @classmethod
        def from_connection_string(cls, conn_str: str, container: str):
            return cls()

        def get_blob_client(self, key):
            return self.blobs.setdefault(key, BlobClientMock())

    def mock_get_client_from_cli_profile(cls, **kwargs):
        return cls()

    monkeypatch.setattr(azure_provider, "ContainerClient", ContainerClientMock)
    monkeypatch.setattr(azure_provider, "BlobServiceClient",
                        BlobServiceClientMock)
    monkeypatch.setattr(azure_provider, "get_client_from_cli_profile",
                        mock_get_client_from_cli_profile)


@pytest.mark.parametrize(
    "data,key,expected,raises",
    [("test", "text_blob.txt", "test", does_not_raise()),
     (b"test", "byte_blob.bin", b"test", does_not_raise()),
     (StringIO("test"), "stream_blob.txt", "test", does_not_raise())])
def test_store(mock_azure_classes, data, key, expected, raises):
    with raises:
        provider = azure_provider.AzureStorageProvider(
            "container", connection_string="test")
        provider.store(data, key)
        assert provider.client.blobs[key].data == expected


def test_retrieve(mock_azure_classes):
    provider = azure_provider.AzureStorageProvider("container",
                                                   connection_string="test")
    provider.store("test", "test.file")
    stream = StringIO()
    provider.retrieve("test.file", stream)
    assert stream.getvalue() == "test"


def test_ls(mock_azure_classes):
    provider = azure_provider.AzureStorageProvider("container",
                                                   connection_string="test")
    provider.store("test", "test.file")
    provider.store("test", "test2.file")
    ls = list(provider.ls())
    assert ls == ["test.file", "test2.file"]
