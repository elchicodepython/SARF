from ..utils import generate_filename
from ..base import (
    StorageDownloader,
    StorageOutput,
    StorageUploader,
    UploadContext,
)


class DummyStorage(StorageUploader, StorageDownloader):
    def print_disclaimer(self):
        print("Dummy Storage in use! Change it in sarf configuration.")

    def upload(
        self, upload_context: UploadContext, content: bytes
    ) -> StorageOutput:
        self.print_disclaimer()
        return StorageOutput("dummy", f"dummy/{generate_filename()}")

    def download(self, path: str) -> bytes:
        self.print_disclaimer()
        return b"Dummy data"
