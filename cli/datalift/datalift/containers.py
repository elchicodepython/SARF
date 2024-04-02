from dependency_injector import containers, providers

from .storages.infra.ftp import FTPStorage
from .storages.infra.s3 import S3Storage
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
        host=config.storage_backend.conf.host,
        basedir=config.storage_backend.conf.basedir,
    )

    s3_storage = providers.Singleton(
        S3Storage,
        access_key=config.storage_backend.conf.access_key,
        secret_key=config.storage_backend.conf.secret_key,
        endpoint_url=config.storage_backend.conf.endpoint_url,
        bucket_name=config.storage_backend.conf.bucket,
    )

    storage = providers.Selector(
        config.storage_backend.type,
        ftp=ftp_storage,
        dummy=dummy_storage,
    )
