import uuid

from .base import UploadContext, Storage, NotificationData
from .notification import UploadNotification


def generate_filename() -> str:
    return f"{uuid.uuid4()}.sarf"


def upload(content: bytes, context: UploadContext, stor: Storage, notification: UploadNotification):
    storage_info = stor.upload(content)
    notification.notify(
        NotificationData(
            context,
            storage_info
        )
    )
