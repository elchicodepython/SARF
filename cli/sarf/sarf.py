#!/usr/bin/env python3

import argparse
import sys
from os import environ
from typing import List, Optional
from .storages.base import Storage, UploadContext
from .notifications.notification import UploadNotification
from .storages.utils import upload

import dependency_injector
from dependency_injector.wiring import Provide, inject

from .containers import Container


welcome_text = """
   ____    _    ____  _____
  / ___|  / \  |  _ \|  ___|
  \___ \ / _ \ | |_) | |_
   ___) / ___ \|  _ <|  _|
  |____/_/   \_\_| \_\_|

  Welcome to SARF - Development edition
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
    tools_storage: Storage=Provide[Container.tools_upload_storage_service],
    upload_notification: UploadNotification=Provide[Container.tools_notification_service],
    emitter: str=Provide[Container.config.messages.emitter]
):
    upload(
        tool_data,
        UploadContext(
            emitter,
            report_id,
            tags
        ),
        tools_storage,
        upload_notification
    )
    if stdout:
        sys.stdout.buffer.write(tool_data)


def get_report_id() -> Optional[str]:
    return environ.get("SARF_REPORT")


def parse_args():
    parser = argparse.ArgumentParser(description="SARF | Security Assesment and Reporting Framework")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Upload the output of a tool to SARF"
    )
    parser.add_argument(
        "--report",
        help="Related report ID. If not provided will be gathered from SARF_REPORT env var"
    )
    parser.add_argument(
        "--tags",
        help="Tags added to tool output message",
        required=False
        )
    parser.add_argument(
        "--stdout",
        help="write ingested data to stdout",
        default=False
    )
    return parser.parse_args()



def process_stdin():
    data = sys.stdin.buffer.read()
    return data


def main():
    container = Container()
    container.wire(modules=[__name__])

    stdin = None
    if not sys.stdin.isatty():
        stdin = process_stdin()

    args = parse_args()

    report_id = args.report or get_report_id()

    tags = []
    if args.tags:
        tags = [tag.strip() for tag in args.tags.split(",")]

    # Ingest data
    if args.ingest:
        errors = False
        if not stdin:
            print("Pipe the output of a tool to SARF")
            errors = True
        if not report_id:
            print("Report ID should be provied with --report param or with SARF_REPORT env var")
            errors = True

        if errors:
            sys.exit(1)
        try:
            publish_tool_output(stdin, report_id, tags, args.stdout)
        except dependency_injector.errors.Error:
            print(
                "Error during dependency injection. Check configuration file")
            print("Configuration file should exist in /etc/sarf/config.yml")
            sys.exit(2)
    else:
        print(welcome_text)
        print("Usage: sarf --help")


if __name__ == "__main__":
    main()
