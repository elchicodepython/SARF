from abc import ABC, abstractmethod


class UploadContext:
    def __init__(self, emitter: str, report_id: str, tags: str):
        self.emitter = emitter
        self.report_id = report_id
        self.tags = tags


class StorageOutput:
    def __init__(self, storage_type: str, path: str):
        self.storage_type = storage_type
        self.path = path


class NotificationData:
    def __init__(self, context: UploadContext, storage_info: StorageOutput):
        self.context = context
        self.storage = storage_info


class Storage(ABC):

    @abstractmethod
    def upload(self, upload_context, content: bytes) -> StorageOutput:
        ...
