from dataclasses import asdict
from typing import Optional, Iterable, Generator, TypeVar, Generic

from .dal.base import DALHandler


T = TypeVar("T")


class SimpleCRUD(Generic[T]):
    def __init__(self, dal_handler: DALHandler, model_class: type):
        self.__dal_handler = dal_handler
        self.__ModelClass = model_class

    def get(self, uuid: str) -> Optional[T]:
        item = self.__dal_handler.get(uuid)
        if item is not None:
            return self.__ModelClass(**item)
        return None

    def get_all(self) -> Iterable[T]:
        items = self.__dal_handler.get_all()
        for item in items:
            yield self.__ModelClass(**item)

    def where(self, conditions: Iterable[dict[str, str]]) -> Iterable[T]:
        items = self.__dal_handler.where(conditions)
        for item in items:
            yield self.__ModelClass(**item)

    def update(self, conditions: Iterable[dict], changes: dict):
        self.__dal_handler.update(conditions, changes)

    def contains(self, field: str, value: str) -> Generator[T, None, None]:
        items = self.__dal_handler.contains(field, value)
        for item in items:
            yield self.__ModelClass(**item)

    def add(self, item: T) -> T:
        return self.__ModelClass(**self.__dal_handler.add(asdict(item)))

    def delete(self, uuid: str):
        self.__dal_handler.delete(uuid)

    def commit(self):
        self.__dal_handler.commit()
