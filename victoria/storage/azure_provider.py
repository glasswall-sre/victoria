"""victoria.storage.azure_provider

Implementation of a StorageProvider for Azure Blob Storage.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from contextlib import contextmanager
from io import IOBase
import logging
from typing import Generator, ContextManager, Union

from azure.storage.blob import ContainerClient

from . import provider


class AzureStorageProvider(provider.StorageProvider):
    """Storage provider for Azure Blob Storage.

    Attributes:
        client (ContainerClient): The Azure API blob client.

    Args:
        connection_string (str): The connection string to the Azure Storage account.
    """
    def __init__(self, connection_string: str, container: str = None):
        self.client = ContainerClient.from_connection_string(
            connection_string, container)

    def store(self, data: Union[IOBase, str, bytes], key: str) -> None:
        blob_client = self.client.get_blob_client(key)
        blob_client.upload_blob(data)

    def retrieve(self, key: str, stream: IOBase):
        blob_client = self.client.get_blob_client(key)
        download_stream = blob_client.download_blob()
        stream.write(download_stream.readall())

    def ls(self) -> Generator[str, None, None]:
        for blob in self.client.list_blobs():
            yield blob.name