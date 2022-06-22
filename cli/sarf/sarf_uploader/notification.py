from awesome_messages.domain.publisher import MessagePublisher
from .base import NotificationData


class UploadNotification:
    def __init__(self, message_pub: MessagePublisher):
        self.__message_pub = message_pub

    def notify(self, upload_output: NotificationData):
        self.__message_pub.publish(
            {
                "emitter": upload_output.context.emitter,
                "report_id": upload_output.context.report_id,
                "tags": upload_output.context.tags,
                "path": upload_output.storage.path
            }
        )
        self.__message_pub.stop_publishing()
