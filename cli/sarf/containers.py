from dependency_injector import containers, providers
from awesome_messages.infra.rabbitmq.publisher import RabbitMessagePublisher

from .sarf_uploader.notification import UploadNotification
from .sarf_uploader.storages.ftp import FTPStorage


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(
        yaml_files=["sarf_config.yml", "/etc/sarf/config.yml"]
        )

    # Messages Objects
    rabbit_publisher = providers.Singleton(
        RabbitMessagePublisher,
        connection_string=config.messages.tools.pub.connection_string,
        queue=config.messages.tools.pub.queue
    )
    messages_tools_publisher = providers.Selector(
        config.messages.tools.pub.type,
        rabbitmq=rabbit_publisher
    )

    # Storage objects
    ftp_storage = providers.Singleton(
        FTPStorage,
        user=config.storage_backend.tools.conf.user,
        password=config.storage_backend.tools.conf.password,
        host=config.storage_backend.tools.conf.host,
        basedir=config.storage_backend.tools.conf.basedir
    )

    tools_storage_service = providers.Selector(
        config.storage_backend.tools.type,
        ftp=ftp_storage
    )

    tools_notification_service = providers.Singleton(
        UploadNotification,
        messages_tools_publisher
    )
