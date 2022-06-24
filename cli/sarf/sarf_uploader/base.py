from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class UploadContext:
    emitter: str
    report_id: str
    tags: str


@dataclass(frozen=True)
class StorageOutput:
    storage_type: str
    path: str


@dataclass(frozen=True)
class NotificationData:
    context: UploadContext
    storage: StorageOutput


class Storage(ABC):

    @abstractmethod
    def upload(self, upload_context, content: bytes) -> StorageOutput:
        ...
