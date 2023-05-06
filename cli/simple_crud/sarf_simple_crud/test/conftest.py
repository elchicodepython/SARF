from unittest.mock import Mock
from typing import Iterable, Optional

from ..dal.base import DALHandler, QueryFilter
from ..simple_crud import SimpleCRUD
from .dummy_class import Dummy

import pytest


class DummyDALHandler(DALHandler):
    def get(self, uuid: str) -> Optional[dict]:
        print(f"Getting item with uuid {uuid}")
        return {"id": uuid, "name": "dummy"}

    def get_all(self) -> Iterable[dict]:
        print("Getting all items")
        return [{"id": "1", "name": "dummy1"}, {"id": "2", "name": "dummy2"}]

    def contains(self, field: str, value: str) -> Iterable[dict]:
        print(f"Checking if field {field} contains value {value}")
        return [{"id": "1", "name": f"0{value.lower()}1"}]

    def where(self, conditions: Iterable[QueryFilter]) -> Iterable[dict]:
        print(f"Filtering items with conditions: {conditions}")
        return [{"id": "1", "name": "dummy1"}]

    def add(self, item: dict) -> dict:
        print(f"Adding item: {item}")
        return {"id": "3", **item}

    update = Mock()

    delete = Mock()

    commit = Mock()


@pytest.fixture
def dummy_dal_handler():
    return DummyDALHandler()

@pytest.fixture
def simple_crud(dummy_dal_handler):
    return SimpleCRUD[Dummy](dummy_dal_handler, Dummy)
