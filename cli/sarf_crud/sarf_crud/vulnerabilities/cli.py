from dependency_injector.wiring import Provide, inject

from ..containers import Container
from .base import Vulnerability, VulnerabilityTemplate
from ..shared.forms.form import Form
from ..shared.cli.crud import handle_cli_crud, CLIFormCrudOperations
from ..shared.cli.forms.form import cli_fields

from sarf_simple_crud.simple_crud import SimpleCRUD


# python 3.7 please to keep dictionary order
vuln_form_base_fields = {
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
        "conf": {"choices": ["WHITE", "GREEN", "AMBER", "RED"]},
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

vuln_form_fields = {
    **vuln_form_base_fields,
    **{
        "evidences": {
            "name": "Evidences",
            "type": "text",
        }
    },
}

vuln_template_form_fields = {
    **vuln_form_base_fields,
    **{
        "lang": {"name": "Lang", "type": "input", "conf": {"default": "en"}},
        "author": {
            "name": "Author",
            "type": "input",
            "conf": {"default": "anonymous"},
        },
    },
}


class VulnerabilityForm(Form):
    """Special form that populates itself with data retrived from
    a vulnerability template.
    """

    def __init__(
        self,
        vuln_crud_handler: SimpleCRUD[Vulnerability],
        vuln_template_crud_handler: SimpleCRUD[VulnerabilityTemplate],
    ):
        super().__init__(cli_fields)
        self._vuln_crud_handler = vuln_crud_handler
        self._vuln_template_crud_handler = vuln_template_crud_handler

    def process_form(self):

        use_template_form = Form(cli_fields)
        use_template_form.set_fields(
            {
                "use_template": {
                    "type": "boolean",
                    "name": "Use template?",
                }
            }
        )

        if use_template_form.process_form()["use_template"]:
            select_template_form = Form(cli_fields)
            select_template_form.set_fields(
                {
                    "template": {
                        "name": "Template",
                        "type": "foreign_search",
                        "conf": {
                            "field": "title",
                            "crud": self._vuln_template_crud_handler,
                            "value_attr": "uuid",
                        },
                    }
                }
            )
            template_data = select_template_form.process_form()
            template_uuid = template_data["template"]
            template = self._vuln_template_crud_handler.get(template_uuid)
            template_fields = template.__dataclass_fields__

            # copy data from template to form fields defaults
            for field in vuln_form_fields:
                if field in template_fields:
                    vuln_form_fields[field].setdefault("conf", {})
                    vuln_form_fields[field]["conf"]["default"] = getattr(
                        template, field
                    )

        vuln_form = Form(cli_fields)
        vuln_form.set_fields(vuln_form_fields)
        return vuln_form.process_form()


class VulnerabilitiesCliController:
    @inject
    def __init__(
        self,
        vuln_crud_handler: SimpleCRUD[Vulnerability] = Provide[
            Container.vulnerabilities_crud  # type: ignore
        ],
        vuln_template_crud_handler: SimpleCRUD[
            VulnerabilityTemplate
        ] = Provide[
            Container.vuln_templates_crud
        ],  # type: ignore
    ):
        self._vuln_crud_handler = vuln_crud_handler
        self._vuln_template_crud_handler = vuln_template_crud_handler

    def handle_request(self, args, stdin):
        form = VulnerabilityForm(
            self._vuln_crud_handler, self._vuln_template_crud_handler
        )
        cli_crud = CLIFormCrudOperations[Vulnerability](
            Vulnerability, self._vuln_crud_handler, form
        )
        if not handle_cli_crud(cli_crud, args):
            # handle not simple crud operations
            pass


class VulnerabilyTemplateCliController:
    @inject
    def __init__(
        self,
        crud_handler: SimpleCRUD[VulnerabilityTemplate] = Provide[
            Container.vuln_templates_crud  # type: ignore
        ],
    ):
        self._crud_handler = crud_handler

    def handle_request(self, args, stdin):
        form = Form(cli_fields)
        form.set_fields(vuln_template_form_fields)
        cli_crud = CLIFormCrudOperations[VulnerabilityTemplate](
            VulnerabilityTemplate,
            self._crud_handler,
            form,
        )
        if not handle_cli_crud(cli_crud, args):
            # handle not simple crud operations
            pass
