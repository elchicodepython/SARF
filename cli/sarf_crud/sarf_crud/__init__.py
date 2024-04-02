from .reports.cli import ReportsCliController
from .vulnerabilities.cli import (
    VulnerabilitiesCliController,
    VulnerabilyTemplateCliController,
)
from .projects.cli import ProjectsCliController


def add_crud_to_parser(parser):
    parser.add_argument("--get", action="store", help="Retrieve a record")
    parser.add_argument(
        "--add",
        action="store",
        help="Add a record. Checkout syntax in sarf docs",
    )
    parser.add_argument(
        "--addi",
        action="store_true",
        help="Add a record in a interactive way",
    )
    parser.add_argument(
        "--delete", action="store", help="Delete a record"
    )
    parser.add_argument(
        "--get-all",
        action="store_true",
        help="List all the records. WARNING: They can be a lot.",
    )



@inject
def get_cli_controllers():
    return {
        "projects": ProjectsCliController(),
        "reports": ReportsCliController(),
        "vulns": VulnerabilitiesCliController(),
        "vuln_templates": VulnerabilyTemplateCliController(),
    }

def init_crud(subparsers):
    reports_parser = subparsers.add_parser("reports")
    reports_parser.add_argument(
        "--get-info", action="store_true", help="Get expanded report data as JSON"
    )
    reports_parser.add_argument(
        "--generate-report", action="store_true", help="Ask a report engine to generate a report"
    )
    reports_parser.add_argument(
        "--add-vuln", help="Add a vulnerability to a report"
    )
    reports_parser.add_argument(
        "--report-engine",
        help="Name of the report engine",
        choices=["js-docx"],
        default="js-docx",
    )
    add_crud_to_parser(reports_parser)

    projects_parser = subparsers.add_parser("projects")
    add_crud_to_parser(projects_parser)

    vulns_parser = subparsers.add_parser("vulns")
    add_crud_to_parser(vulns_parser)

    vuln_templates_parser = subparsers.add_parser("vuln_templates")
    add_crud_to_parser(vuln_templates_parser)