from abc import ABC, abstractmethod
from typing import Optional


class DALHandler(ABC):
    @abstractmethod
    def get(self, uuid: str) -> Optional[dict]:
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
