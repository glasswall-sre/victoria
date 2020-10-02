"""victoria.storage.local_provider

Implementation of a StorageProvider for local file storage.

Author:
    Sam Gibson 
"""
from io import IOBase
import os
from os import path
import shutil
from typing import Generator, Union

from . import provider


class LocalStorageProvider(provider.StorageProvider):
    """Storage provider for local file storage.

    Attributes:
        container (str): The folder we're using to store files in.
    """
    def __init__(self, container: str, **kwargs):
        #pylint: disable=unused-argument
        self.container = container

    def store(self, data: Union[IOBase, str, bytes], key: str) -> None:
        self._ensure_container()
        file_path = path.join(self.container, key)
        if issubclass(type(data), IOBase):
            with open(file_path, "w") as file_handle:
                shutil.copyfileobj(data, file_handle)
        elif type(data) == str:
            with open(file_path, "w") as file_handle:
                file_handle.write(data)
        elif type(data) == bytes:
            with open(file_path, "wb") as file_handle:
                file_handle.write(data)
        else:
            raise TypeError(f"invalid data type '{type(data)}'")

    def retrieve(self, key: str, stream: IOBase) -> None:
        self._ensure_container()
        with open(path.join(self.container, key), "rb") as file_handle:
            shutil.copyfileobj(file_handle, stream)

    def ls(self) -> Generator[str, None, None]:
        self._ensure_container()
        for dirpath, _, filenames in os.walk(self.container):
            for filename in filenames:
                yield path.join(dirpath, filename)

    def _ensure_container(self) -> None:
        os.makedirs(self.container, exist_ok=True)