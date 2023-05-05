from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional


class FilterType(Enum):
    EQ = '='
    GT = '>'
    LT = '<'
    GE = '>='
    LE = '<='
    IN = 'in'


@dataclass
class QueryFilter:
    column: str
    name: str
    value: any


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
    def where(self, conditions: Iterable[QueryFilter]) -> Iterable[dict]:
        pass

    @abstractmethod
    def update(self, conditions: Iterable[QueryFilter], changes: dict):
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
