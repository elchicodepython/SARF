from dependency_injector.wiring import Provide, inject

from ..containers import Container
from .base import Vulnerability, VulnerabilityTemplate
from ..shared.cli.crud import handle_cli_crud, CLIFormCrudOperations
from ..shared.cli.forms.form import cli_form
from ..shared.crud.simple_crud import SimpleCRUD


# python 3.7 please to keep dictionary order
vuln_form_fields = {
    "title": {
        "name": "Title",
        "type": "input",
    },
    "description": {
        "name": "Description",
        "type": "text",
    },
    "tlp": {
        "name": "TLP",
        "type": "select",
        "conf": {
            "choices": [
                "WHITE",
                "GREEN",
                "AMBER",
                "RED"
            ]
        }
    },
    "cvss": {
        "name": "CVSS",
        "type": "input",
    },
    "impact": {
        "name": "Business Impact",
        "type": "text",
    },
    "references": {
        "name": "Vulnerability References",
        "type": "text",
    },
}

vuln_template_form_fields = {
    **vuln_form_fields,
    **{
        "lang": {
            "name": "Lang",
            "type": "input",
            "conf": {
                "default": "en"
            }
        },
        "author": {
            "name": "Author",
            "type": "input",
            "conf": {
                "default": "anonymous"
            }
        },
    }
}


class VulnerabilitiesCliController:
    @inject
    def __init__(self,
        crud_handler: SimpleCRUD[Vulnerability] = Provide[Container.vulnerabilities_crud]
        ):
        self._crud_handler = crud_handler

    def handle_request(self, args, stdin):
        cli_crud = CLIFormCrudOperations[Vulnerability](
            Vulnerability,
            self._crud_handler,
            cli_form,
            vuln_form_fields
        )
        if not handle_cli_crud(cli_crud, args):
            # handle not simple crud operations
            pass


class VulnerabilyTemplateCliController:
    @inject
    def __init__(self,
        crud_handler: SimpleCRUD[VulnerabilityTemplate] = Provide[Container.vuln_templates_crud]
        ):
        self._crud_handler = crud_handler

    def handle_request(self, args, stdin):
        cli_crud = CLIFormCrudOperations[VulnerabilityTemplate](
            VulnerabilityTemplate,
            self._crud_handler,
            cli_form,
            vuln_template_form_fields
        )
        if not handle_cli_crud(cli_crud, args):
            # handle not simple crud operations
            pass
