from dependency_injector import containers, providers
from awesome_messages.domain.publisher import MessagePublisher
from awesome_messages.infra.rabbitmq.publisher import RabbitMessagePublisher

from .notifications.notification import ReportRequestNotification, UploadNotification

from datalift.storages.infra.ftp import FTPStorage
from datalift.storages.infra.s3 import S3Storage
from datalift.storages.infra.dummy import DummyStorage


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(
        yaml_files=["~/.config/sarf_config.yml", "sarf_config.yml", "/etc/sarf/config.yml"]
    )

    # -- Messages --
    # Tools Messages
    tools_rabbit_publisher: MessagePublisher = providers.Singleton(
        RabbitMessagePublisher,
        connection_string=config.messages.tools.pub.connection_string,
        queue=config.messages.tools.pub.queue,
    )

    messages_tools_publisher: MessagePublisher = providers.Selector(
        config.messages.tools.pub.type, rabbitmq=tools_rabbit_publisher
    )

    # Reports Messages
    reports_rabbit_publisher: MessagePublisher = providers.Singleton(
        RabbitMessagePublisher,
        connection_string=config.messages.reports.pub.connection_string,
        queue=config.messages.reports.pub.queue,
    )

    messages_reports_publisher: MessagePublisher = providers.Selector(
        config.messages.reports.pub.type, rabbitmq=reports_rabbit_publisher
    )

    # -- Storage objects --

    dummy_storage = providers.Singleton(DummyStorage)

    # Tools Storage
    tools_ftp_upload_storage = providers.Singleton(
        FTPStorage,
        user=config.storage_backend.tools.upload.conf.user,
        password=config.storage_backend.tools.upload.conf.password,
        host=config.storage_backend.tools.upload.conf.host,
        basedir=config.storage_backend.tools.upload.conf.basedir,
    )

    tools_s3_upload_storage = providers.Singleton(
        S3Storage,
        access_key=config.storage_backend.tools.upload.conf.access_key,
        secret_key=config.storage_backend.tools.upload.conf.secret_key,
        endpoint_url=config.storage_backend.tools.upload.conf.endpoint_url,
        bucket_name=config.storage_backend.tools.upload.conf.bucket,
    )

    tools_upload_storage_service = providers.Selector(
        config.storage_backend.tools.upload.type,
        ftp=tools_ftp_upload_storage,
        s3=tools_s3_upload_storage,
        dummy=dummy_storage,
    )

    # Reports Storage
    reports_ftp_upload_storage = providers.Singleton(
        FTPStorage,
        user=config.storage_backend.reports.upload.conf.user,
        password=config.storage_backend.reports.upload.conf.password,
        host=config.storage_backend.reports.upload.conf.host,
        basedir=config.storage_backend.reports.upload.conf.basedir,
    )

    reports_upload_storage_service = providers.Selector(
        config.storage_backend.reports.upload.type,
        ftp=reports_ftp_upload_storage,
        dummy=dummy_storage,
    )

    # -- Notification objects --
    tools_notification_service = providers.Singleton(
        UploadNotification, messages_tools_publisher
    )
    report_notification_service = providers.Singleton(
        ReportRequestNotification, messages_reports_publisher
    )
