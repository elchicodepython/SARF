from io import BytesIO
from ftplib import FTP, FTP_TLS

from ..utils import generate_filename
from ..base import StorageDownloader, StorageOutput, StorageUploader, UploadContext


class FTPStorage(StorageUploader, StorageDownloader):
    def __init__(self, user: str, password: str, host: str, basedir: str="/", timeout=10, secure=False):
        self.__basedir = basedir
        FTPClass = FTP_TLS if secure else FTP
        self.__client = FTPClass(host, user, password, timeout=timeout)


    def upload(self, context: UploadContext, data: bytes) -> StorageOutput:
        """Upload file to ftp
        """

        # data is bytes but ftp storbinary needs a file like object
        datafile = BytesIO(initial_bytes=data)
        filename = generate_filename()

        with self.__client as ftp:
            ftp.cwd(self.__basedir)
            ftp.storbinary(f"STOR {filename}", datafile)

        return StorageOutput(
            "ftp",
            f"{self.__basedir}/{filename}"
        )

    def download(self, path: str) -> bytes:
        datafile = BytesIO()

        with self.__client as ftp:
            ftp.cwd(self.__basedir)
            ftp.retrbinary(f"STOR {path}", datafile.write)

        return datafile.read()
