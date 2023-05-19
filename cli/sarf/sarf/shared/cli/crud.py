from typing import TypeVar, Generic
import uuid
from dataclasses import asdict
from pprint import pprint

from ..forms.form import Form

from sarf_simple_crud.simple_crud import SimpleCRUD


T = TypeVar("T")


class CLICrudOperations(Generic[T]):
    def __init__(
        self,
        model_class: type,
        crud_handler: SimpleCRUD[T],
        fields=None,
    ):
        self._ModelClass = model_class
        self._crud_handler = crud_handler
        self._fields = fields or {}

    def get(self, uuid):
        model = self._crud_handler.get(uuid)
        if model:
            print("[+] Item found")
            pprint(asdict(model))
        else:
            print("[!] Item not found")

    def get_all(self):
        for item in self._crud_handler.get_all():
            print(f"[+] {item.uuid}: {item}")

    def add(self, content):
        data = self._parse_content(content)
        self._add_uuid_if_needed(data)

        try:
            model = self._ModelClass(**data)
        except TypeError:
            print("[!] Some fields are invalid.")
            return

        self._crud_handler.add(model)
        self._crud_handler.commit()
        print(f"[+] Saved with uuid {model.uuid}")

    def add_interactive(self):
        data = {}
        for field in self._fields:
            value = input(f"[+] {field}: ")
            data[field] = value

        self._add_uuid_if_needed(data)

        model = self._ModelClass(**data)

        self._crud_handler.add(model)
        self._crud_handler.commit()
        print(f"[+] Saved with uuid {model.uuid}")

    def delete(self, uuid):
        self._crud_handler.delete(uuid)
        self._crud_handler.commit()
        print("[+] Done")

    def _add_uuid_if_needed(self, data):
        if "uuid" not in data:
            data["uuid"] = str(uuid.uuid4())

    def _parse_content(self, content: str) -> dict:
        rows = content.split(";")
        data = {}
        for row in rows:
            row_sections = row.split(":")
            data[row_sections[0]] = ":".join(row_sections[1:])
        return data


class CLIFormCrudOperations(CLICrudOperations, Generic[T]):
    def __init__(
        self,
        model_class: type,
        crud_handler: SimpleCRUD[T],
        form: Form,
    ):
        super().__init__(model_class, crud_handler, fields=form.fields)
        self._form = form

    def add_interactive(self):
        data = self._form.process_form()

        self._add_uuid_if_needed(data)
        model = self._ModelClass(**data)

        self._crud_handler.add(model)
        self._crud_handler.commit()
        print(f"[+] Saved with uuid {model.uuid}")


def handle_cli_crud(cli_crud: CLICrudOperations, args):
    if args.get:
        cli_crud.get(args.get)
    elif args.get_all:
        cli_crud.get_all()
    elif args.add:
        cli_crud.add(args.add)
    elif args.addi:
        cli_crud.add_interactive()
    elif args.delete:
        cli_crud.delete(args.delete)
    else:
        return False
    return True
