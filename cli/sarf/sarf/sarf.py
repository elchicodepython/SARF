#!/usr/bin/env python3

import sys
from typing import List

import click

import dependency_injector
from dependency_injector.wiring import Provide, inject

# Previous sarf.storages are now extracted to its own package that
# can be used independently
from datalift.storages.base import Storage
from datalift.storages.utils import generate_filename

from .notifications.notification import UploadNotification
from .notifications.base import UploadNotificationData, UploadContext
from .containers import Container

from . import __version__


@inject
def publish_tool_output(
    tool_data: bytes,
    report_id: str,
    tags: List[str],
    tools_storage: Storage = Provide[Container.tools_upload_storage_service],
    upload_notification: UploadNotification = Provide[
        Container.tools_notification_service
    ],
    emitter: str = Provide[Container.config.messages.emitter],
):
    filename = f"tool_{generate_filename()}.sarf"
    storage_info = tools_storage.upload(filename, tool_data)
    upload_context = UploadContext(emitter=emitter, report_id=report_id, tags=tags)
    upload_notification.notify(UploadNotificationData(upload_context, storage_info))


@inject
def publish_report_output(
    report_data: bytes,
    report_id: str,
    tags: List[str],
    reports_storage: Storage = Provide[
        Container.reports_upload_storage_service
    ],
    upload_notification: UploadNotification = Provide[
        Container.messages_reports_publisher
    ],
    emitter: str = Provide[Container.config.messages.emitter],
):
    filename = f"report_{generate_filename()}.sarf"
    storage_info = reports_storage.upload(filename, report_data)
    upload_context = UploadContext(emitter=emitter, report_id=report_id, tags=tags)
    upload_notification.notify(UploadNotificationData(upload_context, storage_info))


def process_stdin():
    data = sys.stdin.buffer.read()
    return data


def get_bdata_from_filename(filename: str) -> bytes:
    with open(filename, "rb") as f:
        data = f.read()
    return data

@click.group()
def cli():
    pass

@cli.command()
@click.option('--report', help='Report ID', envvar='SARF_REPORT')
@click.option('--tags', help='Tags separated by comma')
@click.option('--filename', help='Filename containing data')
@click.option('--tool', help='Tool in use: nmap, nikto, mobsf...', required=True)
@click.option('--stdout', is_flag=True, help='Print to stdout')
def ingest(report, tags, filename, tool, stdout):

    container = Container()

    container.wire(
        modules=[__name__]
    )

    data = None
    if not sys.stdin.isatty():
        data = process_stdin()

    if tags:
        tags = [tag.strip() for tag in tags.split(",")]
    else:
        tags = []
    
    tags.append(f'tool:{tool}')

    errors = False
    if not data:
        if not filename:
            print("Pipe the output of a tool to SARF or provide a filename with --filename")
            errors = True
        else:
            try:
                data = get_bdata_from_filename(filename)
            except FileNotFoundError:
                print("File not found")
                errors = True

    if errors:
        sys.exit(1)

    if tool == "report":
        publish_report_output(data, report, tags)
    else:
        publish_tool_output(data, report, tags)

    if stdout:
        sys.stdout.buffer.write(data)




def show_outro():
    print('-'*80)
    print('SARF requires a lot of work. Years thinking on it and a ton of nights coding it.')
    print('If you like it please consider supporting the developer behind it.'.center(80))
    print()
    print('--> https://ko-fi.com/elchicodepython <--'.center(80))
    print()
    print('THANK YOU <3'.center(80))
    print('-'*80)

if __name__ == "__main__":
    try:
        cli()
    except (dependency_injector.errors.Error):
        print(
            "Error during dependency injection. Check configuration file"
        )
        print("Configuration file should exist in /etc/sarf/config.yml")
        sys.exit(2)
    show_outro()
