from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class StorageOutput:
    storage_type: str
    path: str


class StorageUploader(ABC):
    @abstractmethod
    def upload(self,path: str, upload_context: dict, content: bytes) -> StorageOutput:
        ...


class StorageDownloader(ABC):
    @abstractmethod
    def download(self, path: str) -> bytes:
        ...


Storage = StorageUploader  # Alias for compatibility reasons
