from dataclasses import asdict
from typing import Iterable

from ...projects.base import Project
from ...vulnerabilities.base import Vulnerability
from ..base import Report


class ReportGenerator:
    def __init__(self, report: Report, project: Project, vulns: Iterable[Vulnerability]):
        self.__report = report
        self.__project = project
        self.__vulns = vulns

    def generate_report(self) -> dict:
        report_data = {
            "project": asdict(self.__project),
            "report": {
                "name": self.__report.name,
                "vulnerabilities": [asdict(vuln) for vuln in self.__vulns]
            },
            
        }
        return report_data
