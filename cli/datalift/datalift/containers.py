from dependency_injector import containers, providers

from .storages.infra.ftp import FTPStorage
from .storages.infra.dummy import DummyStorage


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(
        yaml_files=["data_lift.yml", "/etc/datalift/config.yml"]
    )

    # -- Storage objects --

    dummy_storage = providers.Singleton(DummyStorage)

    ftp_storage = providers.Singleton(
        FTPStorage,
        user=config.storage_backend.conf.user,
        password=config.storage_backend.conf.password,
        host=config.storage_backend.tools.conf.host,
        basedir=config.storage_backend.tools.conf.basedir,
    )

    storage = providers.Selector(
        config.storage_backend.type,
        ftp=ftp_storage,
        dummy=dummy_storage,
    )
