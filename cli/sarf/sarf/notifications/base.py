from dataclasses import dataclass

from sarf.storages.base import UploadContext, StorageOutput


@dataclass(frozen=True)
class UploadNotificationData:
    context: UploadContext
    storage: StorageOutput
