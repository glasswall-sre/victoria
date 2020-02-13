from contextlib import contextmanager
from io import IOBase
import logging
from typing import Generator, ContextManager

from azure.storage.blob.blockblobservice import BlockBlobService

from . import provider


class AzureStorageProvider(provider.StorageProvider):
    def __init__(self, account: str, credential: str, container: str = None):
        self.client = BlockBlobService(account_name=account,
                                       account_key=credential)
        self.container = container

    def store(self, data, key: str) -> None:
        self._ensure_container()
        if issubclass(type(data), IOBase):
            self.client.create_blob_from_stream(self.container, key, data)
        elif type(data) == str:
            self.client.create_blob_from_text(self.container, key, data)
        elif type(data) == bytes:
            self.client.create_blob_from_bytes(self.container, key, data)
        else:
            raise TypeError(f"invalid data type '{type(data)}'")

    def retrieve(self, key: str, stream: IOBase):
        self._ensure_container()
        self.client.get_blob_to_stream(self.container, key, stream)

    def ls(self) -> Generator[str, None, None]:
        self._ensure_container()
        for blob in self.client.list_blobs(self.container):
            yield blob.name

    def _ensure_container(self):
        if not self.container:
            raise ValueError("storage container has not been set")