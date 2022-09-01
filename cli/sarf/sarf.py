#!/usr/bin/env python3

import argparse
import sys
from os import environ
from typing import List, Optional

from .reports.cli import ReportsCliController
from .vulnerabilities.cli import VulnerabilitiesCliController, VulnerabilyTemplateCliController
from .projects.cli import ProjectsCliController

from .storages.base import Storage, UploadContext
from .notifications.notification import UploadNotification
from .storages.utils import upload

import dependency_injector
from dependency_injector.wiring import Provide, inject

from .containers import Container

from . import __version__


welcome_text = f"""
   ____    _    ____  _____
  / ___|  / \  |  _ \|  ___|
  \___ \ / _ \ | |_) | |_
   ___) / ___ \|  _ <|  _|
  |____/_/   \_\_| \_\_|

  Welcome to SARF - version {__version__}
  The Security Assesment and Reporting Framework.

If you like this project please share it and give
a star to it on github. <3

https://github.com/elchicodepython/SARF-Security-Assesment-and-Reporting-Framework
"""


@inject
def publish_tool_output(
    tool_data: bytes,
    project_id: str,
    tags: List[str],
    stdout: bool = False,
    tools_storage: Storage=Provide[Container.tools_upload_storage_service],
    upload_notification: UploadNotification=Provide[Container.tools_notification_service],
    emitter: str=Provide[Container.config.messages.emitter]
):
    upload(
        tool_data,
        UploadContext(
            emitter,
            project_id,
            tags
        ),
        tools_storage,
        upload_notification
    )
    if stdout:
        sys.stdout.buffer.write(tool_data)


@inject
def publish_report_output(
    tool_data: bytes,
    project_id: str,
    tags: List[str],
    tools_storage: Storage=Provide[Container.reports_upload_storage_service],
    upload_notification: UploadNotification=Provide[Container.messages_reports_publisher],
    emitter: str=Provide[Container.config.messages.emitter]
):
    upload(
        tool_data,
        UploadContext(
            emitter,
            project_id,
            tags
        ),
        tools_storage,
        upload_notification
    )

def get_project_id() -> Optional[str]:
    return environ.get("SARF_PROJECT")


def parse_args():
    parser = argparse.ArgumentParser(description="SARF | Security Assesment and Reporting Framework")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Upload an output to SARF"
    )
    parser.add_argument(
        "--filename",
        help="Path of the file to be uploaded"
    )
    parser.add_argument(
        "--project",
        help="Related project ID. If not provided will be gathered from SARF_PROJECT env var"
    )
    parser.add_argument(
        "--tags",
        help="Tags added to the output message",
        required=False
        )
    parser.add_argument(
        "--stdout",
        help="Write the ingested data to stdout",
        default=False
    )
    parser.add_argument(
        "--upload-report",
        action="store_true",
        help="Upload a report to SARF. This flag can be used by third party apps to use SARF uploading configured capabilities"
    )
    parser.add_argument(
        "--report-engine",
        help="Name of the report engine"
    )

    parser.add_argument("--projects", action="store_true")
    parser.add_argument("--vulns", action="store_true")
    parser.add_argument("--vuln-templates", action="store_true")
    parser.add_argument("--reports", action="store_true")

    parser.add_argument("--get", action="store", help="Retrieve a record")
    parser.add_argument("--add", action="store", help="Add a record. Checkout syntax in sarf docs")
    parser.add_argument('--addi', action="store_true", help="Add a record in a interactive way")
    parser.add_argument("--delete", action="store", help="Delete a record")
    parser.add_argument('--get-all', action="store_true", help="List all the records. WARNING: They can be a lot.")

    return parser.parse_args()

def process_stdin():
    data = sys.stdin.buffer.read()
    return data

def get_bdata_from_filename(filename: str) -> bytes:
    with open(filename, 'rb') as f:
        data = f.read()
    return data

def main():
    container = Container()
    container.wire(modules=[
        __name__,
        'sarf.projects.cli',
        'sarf.vulnerabilities.cli',
        'sarf.projects.cli',
        'sarf.reports.cli'])

    data = None
    if not sys.stdin.isatty():
        data = process_stdin()

    args = parse_args()

    project_id = args.project or get_project_id()

    tags = []
    if args.tags:
        tags = [tag.strip() for tag in args.tags.split(",")]

    # Ingest data
    if args.ingest:
        errors = False
        if not data:
            if not args.filename:
                print("Pipe the output of a tool to SARF")
                errors = True
            else:
                try:
                    data = get_bdata_from_filename(args.filename)
                except FileNotFoundError:
                    print("File not found")
                    errors = True

        if not project_id:
            print("Project ID should be provied with --project param or with SARF_PROJECT env var")
            errors = True

        if errors:
            sys.exit(1)
        try:
            if args.upload_report:
                if args.report_engine:
                    tags.append(f'engine:{args.report_engine}')
                publish_report_output(data, project_id, tags)
            else:
                publish_tool_output(data, project_id, tags, args.stdout)
        except dependency_injector.errors.Error:
            print(
                "Error during dependency injection. Check configuration file")
            print("Configuration file should exist in /etc/sarf/config.yml")
            sys.exit(2)
    elif args.projects:
        ProjectsCliController().handle_request(args, data)
    elif args.vulns:
        VulnerabilitiesCliController().handle_request(args, data)
    elif args.vuln_templates:
        VulnerabilyTemplateCliController().handle_request(args, data)
    elif args.reports:
        ReportsCliController().handle_request(args, data)
    else:
        print(welcome_text)
        print("Usage: sarf --help")


if __name__ == "__main__":
    main()
