#!/usr/bin/env python3

import argparse
import sys
import os

from .storages.base import Storage
from .storages.utils import generate_filename
from .containers import Container

import dependency_injector
from dependency_injector.wiring import Provide, inject


@inject
def upload(
    path: str,
    data: bytes,
    tools_storage: Storage = Provide[Container.storage],
):
    tools_storage.upload(path, data)


@inject
def download(
    path: str,
    tools_storage: Storage = Provide[Container.storage],
):
    return tools_storage.download(path)


def process_stdin():
    data = sys.stdin.buffer.read()
    return data


def get_bdata_from_filename(filename: str) -> bytes:
    with open(filename, "rb") as f:
        data = f.read()
    return data


def upload_path(args):
    if args.filename is None:
        if sys.stdin.isatty():
            print("Stop adding data with CTRL+D. Use datalift -h for help.")

        file_data = process_stdin()
    else:
        if not os.path.isfile(args.filename):
            print("Error: File not found.")
            sys.exit(1)
        file_data = get_bdata_from_filename(args.filename)

    if args.stdout:
        sys.stdout.buffer.write(file_data)

    path = args.path or generate_filename()

    upload(path, file_data)
    print(f'Uploaded in {path}')


def download_path(args):
    if args.path is None:
        print("Error: --download option must be accompanied by --path option.")
        sys.exit(1)
    
    data = download(args.path)
    if args.filename:
        with open(args.filename, 'wb') as f:
            f.write(data)
    else:
        print(data, end='')


def get_parser():
    parser = argparse.ArgumentParser(description='Upload and download files or stdout to a file storage.')
    parser.add_argument('filename', nargs='?', type=str, help='name of file')
    parser.add_argument('--download', action='store_true', help='download file from storage')
    parser.add_argument('--stdout', action='store_true', help='print content to stdout')
    parser.add_argument('--path', type=str, help='file uploaded file. uuid generated if not provided')
    return parser


def main():
    container = Container()
    container.wire(
        modules=[
            __name__,
        ]
    )

    args = get_parser().parse_args()

    try:
        if args.download:
            download_path(args)
        else:
            upload_path(args)
    except dependency_injector.errors.Error:
        print('Configuration error. Check datalift docs.')


if __name__ == '__main__':
    main()
