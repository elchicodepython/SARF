from dependency_injector.wiring import Provide, inject

from ..containers import Container
from .base import Report
from ..notifications.notification import ReportRequestNotification
from ..shared.cli.crud import (
    CLIFormCrudOperations,
    handle_cli_crud,
)
from ..shared.cli.forms.form import cli_fields
from ..projects.base import Project
from ..vulnerabilities.base import Vulnerability
from ..shared.forms.form import Form
from ..shared.cli.report_utils import get_report_id_or_print_error
from .app.report import ReportUseCases
from .app.generator import ReportGenerator

from sarf_simple_crud.simple_crud import SimpleCRUD
from sarf_simple_crud.dal.base import QueryFilter, FilterType


class ReportsCliController:
    @inject
    def __init__(
        self,
        crud_handler: SimpleCRUD[Report] = Provide[Container.reports_crud],  # type: ignore
        projects_crud: SimpleCRUD[Project] = Provide[Container.projects_crud],  # type: ignore
        vulns_crud: SimpleCRUD[Vulnerability] = Provide[Container.vulnerabilities_crud],  # type: ignore
        report_request_notificator: ReportRequestNotification = Provide[Container.report_notification_service],  # type: ignore
    ):
        self._crud_handler = crud_handler
        self._projects_crud = projects_crud
        self._vulns_crud = vulns_crud
        self._use_cases = ReportUseCases(crud_handler)
        self._request_generate_report = report_request_notificator

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
            report_id = get_report_id_or_print_error()
            if not report_id:
                return

            if any([args.get_info, args.generate_report]):
                vulns = self._vulns_crud.where(
                    [
                        QueryFilter("uuid", FilterType.IN, self._use_cases.get_report(
                                report_id
                            ).vulnerabilities)
                    ]
                )
                report = self._crud_handler.get(report_id)
                project = self._projects_crud.get(report.project)
                report_data = ReportGenerator(report, project, vulns).generate_report()
                if args.get_info:
                    print(report_data)
                else:
                    self._request_generate_report.notify(report_data)

            elif args.add_vuln:
                vulns = self._vulns_crud.where(
                    [
                        QueryFilter("uuid", FilterType.EQ, args.add_vuln)
                    ]
                )
                if list(vulns):
                    self._use_cases.add_vuln(
                        report_id,
                        args.add_vuln
                    )
                else:
                    print("Vulnerability doesn't exist")
