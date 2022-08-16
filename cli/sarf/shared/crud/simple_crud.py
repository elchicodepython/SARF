from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Optional
from typing import TypeVar, Generic


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


T = TypeVar('T')


class SimpleCRUD(Generic[T]):

    def __init__(self, dal_handler: DALHandler, model_class: type):
        self.__dal_handler = dal_handler
        self.__ModelClass = model_class

    def get(self, uuid: str) -> Optional[T]:
        item = self.__dal_handler.get(uuid)
        if item is not None:
            return self.__ModelClass(**item)

    def add(self, item: T) -> T:
       return self.__ModelClass(**self.__dal_handler.add(asdict(item)))

    def delete(self, uuid: str):
        self.__dal_handler.delete(uuid)

    def commit(self):
        self.__dal_handler.commit()
