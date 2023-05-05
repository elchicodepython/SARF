import json
from typing import Dict, Iterable, Optional

from ..base import DALHandler, QueryFilter, FilterType


class JSONDatabase(DALHandler):
    """Manages a JSON file like a database"""

    def __init__(self, filename: str):
        self.__filename = filename
        try:
            with open(filename) as data_file:
                self.__data: Dict = json.loads(data_file.read())
        except FileNotFoundError:
            self.__data = {}

    def get(self, uuid: str) -> Optional[dict]:
        return self.__data.get(uuid)

    def get_all(self) -> Iterable[dict]:
        return self.__data.values()

    def where(self, conditions: Iterable[QueryFilter]) -> Iterable[dict]:

        filter_dispatch = {
                FilterType.EQ: lambda row, condition: row[condition["field"]] == condition["value"],
                FilterType.GT: lambda row, condition: row[condition["field"]] > condition["value"],
                FilterType.LT: lambda row, condition: row[condition["field"]] < condition["value"],
                FilterType.GE: lambda row, condition: row[condition["field"]] >= condition["value"],
                FilterType.LE: lambda row, condition: row[condition["field"]] <= condition["value"],
                FilterType.IN: lambda row, condition: condition["value"] in row[condition["field"]],
            }

        for row in self.__data.values():
            if all(filter_dispatch[condition.name](row, condition) for condition in conditions):
                yield row

    def contains(self, field: str, value: str) -> Iterable[dict]:
        return [
            row
            for row in self.get_all()
            if value.lower() in row[field].lower()
        ]

    def update(self, conditions: Iterable[QueryFilter], changes: dict):
        for row in self.where(conditions):
            updated_row = {**row}
            for change_key, change_value in changes.items():
                updated_row[change_key] = change_value
            self.__data[row["uuid"]] = updated_row

    def add(self, item: dict) -> dict:
        if item["uuid"] in self.__data:
            raise Exception("Identifier already exist")
        self.__data[item["uuid"]] = item
        return item

    def delete(self, uuid: str):
        self.__data.pop(uuid)

    def commit(self):
        with open(self.__filename, "wt") as data_file:
            data_file.write(json.dumps(self.__data))
