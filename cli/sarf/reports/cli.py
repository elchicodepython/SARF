from dependency_injector.wiring import Provide, inject

from ..containers import Container
from .base import Report
from ..shared.cli.crud import (
    CLIFormCrudOperations,
    handle_cli_crud,
    CLICrudOperations,
)
from ..shared.crud.simple_crud import SimpleCRUD
from ..shared.cli.forms.form import cli_fields
from ..projects.base import Project
from ..shared.forms.form import Form


class ReportsCliController:
    @inject
    def __init__(
        self,
        crud_handler: SimpleCRUD[Report] = Provide[Container.reports_crud],
        projects_crud: SimpleCRUD[Project] = Provide[Container.projects_crud],
    ):
        self._crud_handler = crud_handler
        self._projects_crud = projects_crud

    def handle_request(self, args, stdin):
        form = Form(cli_fields)
        form.set_fields(
            {
                "project": {
                    "name": "Project",
                    "type": "foreign_search",
                    "conf": {
                        "field": "name",
                        "crud": self._projects_crud,
                        "value_attr": "uuid",
                    },
                },
                "name": {"name": "Report name", "type": "input"},
            }
        )

        cli_crud = CLIFormCrudOperations[Report](
            Report, self._crud_handler, form
        )
        if not handle_cli_crud(cli_crud, args):
            # handle not simple crud operations
            pass
