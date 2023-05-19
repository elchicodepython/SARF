from dependency_injector import containers, providers
from awesome_messages.domain.publisher import MessagePublisher
from awesome_messages.infra.rabbitmq.publisher import RabbitMessagePublisher

from .notifications.notification import ReportRequestNotification, UploadNotification
from .reports.base import Report
from .vulnerabilities.base import Vulnerability, VulnerabilityTemplate
from .projects.base import Project

from datalift.storages.infra.ftp import FTPStorage
from datalift.storages.infra.dummy import DummyStorage
from sarf_simple_crud.simple_crud import SimpleCRUD
from sarf_simple_crud.dal.infra.json_dal import JSONDatabase


class Container(containers.DeclarativeContainer):

    config = providers.Configuration(
        yaml_files=["sarf_config.yml", "/etc/sarf/config.yml"]
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

    tools_upload_storage_service = providers.Selector(
        config.storage_backend.tools.upload.type,
        ftp=tools_ftp_upload_storage,
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

    # -- CRUD objects --

    # Projects
    projects_dal = providers.Selector(
        config.crud.projects.type,
        json=providers.Singleton(
            JSONDatabase, filename=config.crud.projects.conf.filename
        ),
    )

    projects_crud = providers.Singleton(SimpleCRUD, projects_dal, Project)

    # Vulnerabilities
    vulnerabilities_dal = providers.Selector(
        config.crud.vulnerabilities.type,
        json=providers.Singleton(
            JSONDatabase, filename=config.crud.vulnerabilities.conf.filename
        ),
    )

    vulnerabilities_crud = providers.Singleton(
        SimpleCRUD, vulnerabilities_dal, Vulnerability
    )

    vuln_templates = providers.Selector(
        config.crud.vulnerabilities.type,
        json=providers.Singleton(
            JSONDatabase, filename=config.crud.vuln_templates.conf.filename
        ),
    )

    vuln_templates_crud = providers.Singleton(
        SimpleCRUD, vuln_templates, VulnerabilityTemplate
    )

    # Reports
    reports_dal = providers.Selector(
        config.crud.reports.type,
        json=providers.Singleton(
            JSONDatabase, filename=config.crud.reports.conf.filename
        ),
    )

    reports_crud = providers.Singleton(SimpleCRUD, reports_dal, Report)
