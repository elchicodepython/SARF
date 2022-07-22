from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class UploadContext:
    emitter: str
    report_id: str
    tags: List[str]


@dataclass(frozen=True)
class StorageOutput:
    storage_type: str
    path: str


class StorageUploader(ABC):

    @abstractmethod
    def upload(self, upload_context, content: bytes) -> StorageOutput:
        ...


class StorageDownloader(ABC):

    @abstractmethod
    def download(self, path: str) -> bytes:
        ...


Storage = StorageUploader # Alias for compatibility reasons
