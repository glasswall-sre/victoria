"""victoria.storage.azure_provider

Implementation of a StorageProvider for Azure Blob Storage.

Author:
    Sam Gibson 
"""
from io import IOBase
import logging
from typing import Generator, Union

from azure.common.client_factory import get_client_from_cli_profile
from azure.storage.blob import BlobServiceClient

from . import provider


class AzureStorageProvider(provider.StorageProvider):
    """Storage provider for Azure Blob Storage.

    Attributes:
        main_client (BlobServiceClient): The Azure blob service client.
        client (ContainerClient): The Azure API blob client.

    Args:
        container (str): The storage container to use.
        auth_via_cli (bool): Whether we should authenticate via the Azure CLI.
        account_name (str): The name of the storage account. Only used if auth via CLI.
        connection_string (str): The connection string to the Azure Storage account. Only used if not auth via CLI.
    """
    def __init__(self,
                 container: str,
                 auth_via_cli: bool = False,
                 account_name: str = "",
                 connection_string: str = ""):
        if auth_via_cli:
            if not account_name:
                logging.error(
                    "ERROR: Need to specify 'account_name' for "
                    "Azure storage provider when authenticating via Azure CLI")
                raise SystemExit(1)
            try:
                self.main_client = get_client_from_cli_profile(
                    BlobServiceClient,
                    account_url=f"https://{account_name}.blob.core.windows.net/"
                )

            except ImportError as err:
                logging.error(
                    "ERROR: Unable to authenticate via Azure CLI, have you "
                    "logged in with 'az login'?")
                raise SystemExit(1) from err
        else:
            if not connection_string:
                logging.error(
                    "ERROR: Need to specify 'connection_string' for "
                    "Azure storage provider when not authenticating via Azure CLI"
                )
                raise SystemExit(1)
            self.main_client = BlobServiceClient.from_connection_string(
                connection_string)

        self.client = self.main_client.get_container_client(container)

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