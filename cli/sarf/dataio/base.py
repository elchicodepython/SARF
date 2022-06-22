from abc import ABC


class Output(ABC):
    def write(self, content: bytes) -> None:
        ...

    def writeText(self, content: str) -> None:
        ...


class Input(ABC):
    def retrieve(self) -> str:
        ...
