from awesome_messages.domain.publisher import MessagePublisher
from .base import UploadNotificationData


class UploadNotification:
    def __init__(self, message_pub: MessagePublisher):
        self.__message_pub = message_pub

    def notify(self, upload_output: UploadNotificationData):
        self.__message_pub.publish(
            {
                "emitter": upload_output.context.emitter,
                "report_id": upload_output.context.report_id,
                "tags": upload_output.context.tags,
                "storage_type": upload_output.storage.storage_type,
                "path": upload_output.storage.path,
            }
        )
        self.__message_pub.stop_publishing()


class ReportRequestNotification:
    def __init__(self, message_pub: MessagePublisher):
        self.__message_pub = message_pub

    def notify(self, upload_output: dict):
        self.__message_pub.publish(
            upload_output
        )
        self.__message_pub.stop_publishing()
