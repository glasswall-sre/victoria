"""victoria.storage.azure_provider

Implementation of a StorageProvider for Azure Blob Storage.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from contextlib import contextmanager
from io import IOBase
import logging
from typing import Generator, ContextManager, Union

from azure.storage.blob.blockblobservice import BlockBlobService

from . import provider


class AzureStorageProvider(provider.StorageProvider):
    """Storage provider for Azure Blob Storage.

    Attributes:
        client (BlockBlobService): The Azure API blob client.
        container (str): The container we are currently using.

    Args:
        account (str): The storage account name to connect to.
        credential (str): The connection string of the storage account.
        container (str): The container within the account to focus on.
    """
    def __init__(self, account: str, credential: str, container: str = None):
        self.client = BlockBlobService(account_name=account,
                                       account_key=credential)
        self.container = container

    def store(self, data: Union[IOBase, str, bytes], key: str) -> None:
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
        """Ensure that we are actually connected to a container."""
        if not self.container:
            raise ValueError("storage container has not been set")