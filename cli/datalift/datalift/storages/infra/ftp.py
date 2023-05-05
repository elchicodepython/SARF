from io import BytesIO
from ftplib import FTP, FTP_TLS

from ..base import (
    StorageDownloader,
    StorageOutput,
    StorageUploader,
)


class FTPStorage(StorageUploader, StorageDownloader):
    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        basedir: str = "/",
        timeout=10,
        secure=False,
    ):
        self.__basedir = basedir
        FTPClass = FTP_TLS if secure else FTP
        self.__client = FTPClass(host, user, password, timeout=timeout)

    def upload(self, path: str, data: bytes) -> StorageOutput:
        """Upload file to ftp"""

        # data is bytes but ftp storbinary needs a file like object
        datafile = BytesIO(initial_bytes=data)

        with self.__client as ftp:
            ftp.cwd(self.__basedir)
            ftp.storbinary(f"STOR {path}", datafile)

        return StorageOutput("ftp", f"{self.__basedir}/{path}")

    def download(self, path: str) -> bytes:
        datafile = BytesIO()

        with self.__client as ftp:
            ftp.cwd(self.__basedir)
            ftp.retrbinary(f"STOR {path}", datafile.write)

        return datafile.read()
