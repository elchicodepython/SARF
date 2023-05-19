from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class UploadContext:
    emitter: str
    report_id: str
    tags: List[str]


@dataclass(frozen=True)
class StorageOutput:
    storage_type: str
    path: str


@dataclass(frozen=True)
class UploadNotificationData:
    context: UploadContext
    storage: StorageOutput
