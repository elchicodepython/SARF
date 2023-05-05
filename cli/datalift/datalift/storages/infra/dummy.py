from ..utils import generate_filename
from ..base import (
    StorageDownloader,
    StorageOutput,
    StorageUploader,
)


class DummyStorage(StorageUploader, StorageDownloader):
    def print_disclaimer(self):
        print("Dummy Storage in use! Change it in configuration.")

    def upload(
        self, path: str, content: bytes
    ) -> StorageOutput:
        self.print_disclaimer()
        return StorageOutput("dummy", f"dummy/{generate_filename()}")

    def download(self, path: str) -> bytes:
        self.print_disclaimer()
        return b"Dummy data"
