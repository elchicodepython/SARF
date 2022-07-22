from dependency_injector import containers, providers
from awesome_messages.domain.publisher import MessagePublisher
from awesome_messages.infra.rabbitmq.publisher import RabbitMessagePublisher

from .notifications.notification import UploadNotification
from .storages.infra.ftp import FTPStorage


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(
        yaml_files=["sarf_config.yml", "/etc/sarf/config.yml"]
        )

    # Messages Objects
    rabbit_publisher: MessagePublisher = providers.Singleton(
        RabbitMessagePublisher,
        connection_string=config.messages.tools.pub.connection_string,
        queue=config.messages.tools.pub.queue
    )
    messages_tools_publisher: MessagePublisher = providers.Selector(
        config.messages.tools.pub.type,
        rabbitmq=rabbit_publisher
    )

    # Storage objects
    ftp_upload_storage = providers.Singleton(
        FTPStorage,
        user=config.storage_backend.tools.upload.conf.user,
        password=config.storage_backend.tools.upload.conf.password,
        host=config.storage_backend.tools.upload.conf.host,
        basedir=config.storage_backend.tools.upload.conf.basedir
    )

    tools_upload_storage_service = providers.Selector(
        config.storage_backend.tools.upload.type,
        ftp=ftp_upload_storage
    )

    tools_notification_service = providers.Singleton(
        UploadNotification,
        messages_tools_publisher
    )
