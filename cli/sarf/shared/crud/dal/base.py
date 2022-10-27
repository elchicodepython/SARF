from abc import ABC, abstractmethod
from typing import Iterable, Optional


class DALHandler(ABC):
    @abstractmethod
    def get(self, uuid: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_all(self) -> Iterable[dict]:
        pass

    @abstractmethod
    def contains(self, field: str, value: str) -> Iterable[dict]:
        pass

    @abstractmethod
    def where(self, conditions: Iterable[dict]) -> Iterable[dict]:
        pass

    @abstractmethod
    def add(self, item: dict) -> dict:
        pass

    @abstractmethod
    def delete(self, uuid: str):
        pass

    @abstractmethod
    def commit(self):
        pass
