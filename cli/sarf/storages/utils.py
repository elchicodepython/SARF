import uuid

from .base import UploadContext, Storage
from ..notifications.base import UploadNotificationData
from ..notifications.notification import UploadNotification


def generate_filename() -> str:
    return f"{uuid.uuid4()}.sarf"


def upload(content: bytes, context: UploadContext, stor: Storage, notification: UploadNotification):
    storage_info = stor.upload(context, content)
    notification.notify(
        UploadNotificationData(
            context,
            storage_info
        )
    )
