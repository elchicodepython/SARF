#!/usr/bin/env python3

import argparse
import sys
from typing import List


from .reports.cli import ReportsCliController
from .vulnerabilities.cli import (
    VulnerabilitiesCliController,
    VulnerabilyTemplateCliController,
)
from .projects.cli import ProjectsCliController

from .notifications.notification import UploadNotification
from .notifications.base import UploadNotificationData, UploadContext
from .shared.cli.report_utils import get_report_id

import dependency_injector
from dependency_injector.wiring import Provide, inject

# Previous sarf.storages are now extracted to its own package that
# can be used independently
from datalift.storages.base import Storage
from datalift.storages.utils import generate_filename

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
    report_id: str,
    tags: List[str],
    stdout: bool = False,
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
    if stdout:
        sys.stdout.buffer.write(tool_data)


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


def parse_args():
    def add_crud_to_parser(parser):
        parser.add_argument("--get", action="store", help="Retrieve a record")
        parser.add_argument(
            "--add",
            action="store",
            help="Add a record. Checkout syntax in sarf docs",
        )
        parser.add_argument(
            "--addi",
            action="store_true",
            help="Add a record in a interactive way",
        )
        parser.add_argument(
            "--delete", action="store", help="Delete a record"
        )
        parser.add_argument(
            "--get-all",
            action="store_true",
            help="List all the records. WARNING: They can be a lot.",
        )

    parser = argparse.ArgumentParser(
        description="SARF | Security Assesment and Reporting Framework"
    )
    subparsers = parser.add_subparsers(dest="main_command")
    parser.add_argument(
        "--ingest", action="store_true", help="Upload an output to SARF"
    )
    parser.add_argument("--filename", help="Path of the file to be uploaded")
    parser.add_argument(
        "--report",
        help="Related report ID. If not provided will be gathered from SARF_REPORT env var",
    )
    parser.add_argument(
        "--tags", help="Tags added to the output message", required=False
    )
    parser.add_argument(
        "--stdout", help="Write the ingested data to stdout", default=False
    )
    parser.add_argument(
        "--upload-report",
        action="store_true",
        help="Upload a report to SARF. This flag can be used by third party apps to use SARF uploading configured capabilities",
    )

    reports_parser = subparsers.add_parser("reports")
    reports_parser.add_argument(
        "--get-info", action="store_true", help="Get expanded report data as JSON"
    )
    reports_parser.add_argument(
        "--generate-report", action="store_true", help="Ask a report engine to generate a report"
    )
    reports_parser.add_argument(
        "--add-vuln", help="Add a vulnerability to a report"
    )
    reports_parser.add_argument(
        "--report-engine",
        help="Name of the report engine",
        choices=["js-docx"],
        default="js-docx",
    )
    add_crud_to_parser(reports_parser)

    projects_parser = subparsers.add_parser("projects")
    add_crud_to_parser(projects_parser)

    vulns_parser = subparsers.add_parser("vulns")
    add_crud_to_parser(vulns_parser)

    vuln_templates_parser = subparsers.add_parser("vuln_templates")
    add_crud_to_parser(vuln_templates_parser)

    return parser.parse_args()


def process_stdin():
    data = sys.stdin.buffer.read()
    return data


def get_bdata_from_filename(filename: str) -> bytes:
    with open(filename, "rb") as f:
        data = f.read()
    return data


@inject
def get_cli_controllers():
    return {
        "projects": ProjectsCliController(),
        "reports": ReportsCliController(),
        "vulns": VulnerabilitiesCliController(),
        "vuln_templates": VulnerabilyTemplateCliController(),
    }


def main():
    container = Container()
    container.wire(
        modules=[
            __name__,
            "sarf.projects.cli",
            "sarf.vulnerabilities.cli",
            "sarf.projects.cli",
            "sarf.reports.cli",
        ]
    )

    data = None
    if not sys.stdin.isatty():
        data = process_stdin()

    args = parse_args()

    report_id = args.report or get_report_id()

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

        if not report_id:
            print(
                "Report ID should be provied with --report param or with SARF_REPORT env var"
            )
            errors = True

        if errors:
            sys.exit(1)
        try:
            if args.upload_report:
                if args.report_engine:
                    tags.append(f"engine:{args.report_engine}")
                publish_report_output(data, report_id, tags)
            else:
                publish_tool_output(data, report_id, tags, args.stdout)
        except dependency_injector.errors.Error:
            print(
                "Error during dependency injection. Check configuration file"
            )
            print("Configuration file should exist in /etc/sarf/config.yml")
            sys.exit(2)
    elif cli_controller := get_cli_controllers().get(args.main_command):
        cli_controller.handle_request(args, data)
    else:
        print(welcome_text)
        print("Usage: sarf --help")


if __name__ == "__main__":
    main()
