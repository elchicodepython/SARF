#!/usr/bin/env python3

import argparse
import sys
from os import environ
from typing import List
from sarf_uploader.base import Storage, UploadContext
from sarf_uploader.notification import UploadNotification

from dependency_injector.wiring import Provide, inject

from containers import Container

from sarf_uploader.utils import upload


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
    tools_storage: Storage=Provide[Container.tools_storage_service],
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


def get_report_id() -> str:
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
    return parser.parse_args()



def process_stdin():
    data = sys.stdin.buffer.read()
    return data


if __name__ == "__main__":
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

        publish_tool_output(stdin, report_id, tags)

    else:
        print(welcome_text)
