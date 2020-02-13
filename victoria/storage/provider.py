from abc import ABC, abstractmethod
from io import IOBase
from typing import Generator, ContextManager


class StorageProvider(ABC):
    @abstractmethod
    def store(self, data, key: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    def retrieve(self, key: str, stream: IOBase) -> None:
        raise NotImplementedError()

    @abstractmethod
    def ls(self) -> Generator[str, None, None]:
        raise NotImplementedError()