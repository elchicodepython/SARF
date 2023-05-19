from typing import Generic, TypeVar, Iterable
from PyInquirer import prompt

from sarf_simple_crud.simple_crud import SimpleCRUD


class InputField:
    def __init__(self, style=None):
        self.__style = style

    def parse_data(self, name, conf=None):
        conf = conf or {}
        inquirer_field_structure = {
            "type": "input",
            "name": name,
            "message": name,
            "default": conf.get("default", ""),
        }
        data = prompt([inquirer_field_structure], style=self.__style)
        return data[name]


class TextField:
    def __init__(self, style=None, editor="vim"):
        self.__editor = editor
        self.__style = style

    def parse_data(self, name, conf=None):
        print(f'Press enter to write "{name}" in a text editor')
        input()
        conf = conf or {}
        inquirer_field_structure = {
            "type": "editor",
            "name": name,
            "eargs": {"editor": self.__editor},
            "message": name,
            "default": conf.get("default", ""),
        }
        data = prompt([inquirer_field_structure], style=self.__style)

        value = data[name]
        if conf.get("value_attr"):
            value = getattr(value, conf["value_attr"])

        return value


class SelectField:
    def __init__(self, style=None):
        self.__style = style

    def parse_data(self, name, conf=None):
        conf = conf or {}
        inquirer_field_structure = {
            "type": "list",
            "name": name,
            "message": name,
            "choices": conf.get("choices", []),
        }
        data = prompt([inquirer_field_structure], style=self.__style)
        return data[name]


class BooleanField:
    def __init__(self, style=None):
        self.__style = style

    def parse_data(self, name, conf=None):
        conf = conf or {}
        inquirer_field_structure = {
            "type": "confirm",
            "name": name,
            "message": name,
            "default": conf.get("default", True),
        }
        data = prompt([inquirer_field_structure], style=self.__style)
        return data[name]


T = TypeVar("T")


class ForeignSelectField(Generic[T]):
    def __init__(self, style=None):
        self.__style = style

    def search_items(
        self, search_field: str, crud: SimpleCRUD
    ) -> Iterable[T]:
        selecting_opts = True
        while selecting_opts:
            field_value = input(f"{search_field} to search: ")
            items = crud.contains(search_field, field_value)
            items_list = list(items)
            response = input(
                f"Found {len(items_list)} items. Continue? [Y]: "
            )
            response = response.lower().strip()
            if response in ("y", ""):
                selecting_opts = False

        return items_list

    def parse_data(self, name, conf=None):

        conf = conf or {}

        if not conf.get("crud"):
            raise ValueError("crud parametter required in field conf")

        print(f"In the next step you are going to search for a {name}")
        searching = True

        while searching:
            choices = [
                {"name": str(item), "value": item}
                for item in self.search_items(conf["field"], conf["crud"])
            ]
            choices.append(
                {"name": "None of them. Repeat search.", "value": "none"}
            )

            inquirer_field_structure = {
                "type": "list",
                "name": name,
                "message": name,
                "choices": conf.get("choices", choices),
            }
            data = prompt([inquirer_field_structure], style=self.__style)
            if data[name] != "none":
                searching = False

        value = data[name]
        if conf.get("value_attr"):
            value = getattr(value, conf["value_attr"])

        return value
