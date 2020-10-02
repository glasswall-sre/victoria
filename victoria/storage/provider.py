"""victoria.storage.provider

Abstract base class of a storage provider.

Author:
    Sam Gibson 
"""
from abc import ABC, abstractmethod
from io import IOBase
from typing import Generator, Union


class StorageProvider(ABC):
    """Abstract base class of a storage provider."""
    @abstractmethod
    def store(self, data: Union[IOBase, str, bytes], key: str) -> None:
        """Store a piece of data at a given key in blob storage.

        Args:
            data: The data to store.
            key: The path within the container to store it in.
        """
        raise NotImplementedError()

    @abstractmethod
    def retrieve(self, key: str, stream: IOBase) -> None:
        """Retrieve a piece of data from a given key in blob storage.

        Args:
            key: The key within the container to get the data from.
            stream: The stream to stream the data into.
        """
        raise NotImplementedError()

    @abstractmethod
    def ls(self) -> Generator[str, None, None]:
        """List blobs within a container.

        Yields:
            str: The names of blobs within the container.
        """
        raise NotImplementedError()