from dependency_injector import containers, providers

from awesome_messages.domain.listener import MessageListener
from awesome_messages.infra.rabbitmq.listener import RabbitMessageListener
from sarf.containers import Container as MainContainer

from sarf.sarf_uploader.storages.ftp import FTPStorage


class ListenerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    data = providers.Singleton(
        dict,
        config.listeners
    )

    # Messages Objects
    rabbit_listener: MessageListener = providers.Singleton(
        RabbitMessageListener,
        connection_string=config.messages.tools.sub.connection_string,
        queue=config.messages.tools.sub.queue,
    )

    messages_tools_subscriber: MessageListener = providers.Selector(
        config.messages.tools.sub.type,
        rabbitmq=rabbit_listener,
    )

    # Storage objects
    ftp_download_storage = providers.Singleton(
        FTPStorage,
        user=config.storage_backend.tools.download.conf.user,
        password=config.storage_backend.tools.download.conf.password,
        host=config.storage_backend.tools.download.conf.host,
        basedir=config.storage_backend.tools.download.conf.basedir
    )

    tools_download_storage_service = providers.Selector(
        config.storage_backend.tools.download.type,
        ftp=ftp_download_storage
    )


class Application(containers.DeclarativeContainer):

    config = providers.Configuration(
        yaml_files=["/etc/sarf/config.yml"]
    )

    core = providers.Container(
        MainContainer,
        config=config
    )

    listener = providers.Container(
        ListenerContainer,
        config=config
    )
