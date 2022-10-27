from dependency_injector.wiring import Provide, inject

from ..containers import Container
from .base import Report
from ..shared.cli.crud import (
    CLIFormCrudOperations,
    handle_cli_crud,
)
from ..shared.crud.simple_crud import SimpleCRUD
from ..shared.cli.forms.form import cli_fields
from ..projects.base import Project
from ..vulnerabilities.base import Vulnerability
from ..shared.forms.form import Form


class ReportsCliController:
    @inject
    def __init__(
        self,
        crud_handler: SimpleCRUD[Report] = Provide[Container.reports_crud],  # type: ignore
        projects_crud: SimpleCRUD[Project] = Provide[Container.projects_crud],  # type: ignore
        vulns_crud: SimpleCRUD[Vulnerability] = Provide[Container.vulnerabilities_crud],  # type: ignore
    ):
        self._crud_handler = crud_handler
        self._projects_crud = projects_crud
        self._vulns_crud = vulns_crud

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
            if args.generate_report:
                print("[+] Sending message to generate report")
                vulns = self._vulns_crud.where(
                    [
                        {
                            "field": "uuid",
                            "op": "in",
                            "value": args.generate_report,
                        }
                    ]
                )
                print(list(vulns))
