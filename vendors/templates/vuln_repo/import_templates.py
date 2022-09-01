import json
import uuid

from dependency_injector.wiring import Provide, inject

from sarf.vulnerabilities.base import VulnerabilityTemplate
from sarf.shared.crud.simple_crud import SimpleCRUD
from sarf.containers import Container


vulns_file = "assets/vulns.json"


@inject
def import_vulns(vulns_file,
                crud_handler: SimpleCRUD[VulnerabilityTemplate] = Provide[Container.vuln_templates_crud]):

    with open(vulns_file) as vulnrepo_templates:
        vulns = json.loads(vulnrepo_templates.read())

    sarf_vulns = [
        VulnerabilityTemplate(
            uuid = str(uuid.uuid4()),
            title = vuln["title"],
            cvss = vuln["cvss"],
            references = vuln["ref"],
            description = vuln["desc"],
            impact = "",
            tlp = "WHITE",
            lang = "en",
            author = "[vulnrepo]"
        ) for vuln in vulns
    ]

    for vuln in sarf_vulns:
        print(f"Importing {vuln.title}")
        crud_handler.add(vuln)
    crud_handler.commit()


def main():
    container = Container()
    container.wire(modules=[__name__])
    import_vulns(vulns_file)

if __name__ == "__main__":
    main()
