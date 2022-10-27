from abc import ABC, abstractmethod
from typing import Dict


class FieldsRegistry:
    def __init__(self):
        self.__fields = {}

    def add(self, field, field_type):
        self.__fields[field_type] = field

    def get(self, field_type):
        return self.__fields[field_type]


class Form:
    def __init__(self, fields_registry: FieldsRegistry):
        self.__fields_registry = fields_registry
        self.__form_fields: Dict = {}

    def set_fields(self, fields: dict):
        self.__form_fields = fields

    @property
    def fields(self):
        return self.__form_fields

    def process_form(self):
        data = {}
        for field_key in self.__form_fields:
            field = self.__form_fields[field_key]
            value = self.__fields_registry.get(field["type"]).parse_data(
                field["name"], field.get("conf")
            )
            data[field_key] = value
        return data


class FormFactory(ABC):
    @abstractmethod
    def create_form(self, form_fields) -> Form:
        pass
