from io import BytesIO
from typing import List

from projects.base import Project
from ..base import Report, ReportStatus, ReportEngine


class DummyReport(Report):
    def __init__(self):
        self.__report_status = ReportStatus.REQUESTED

    def get_status(self):
        response = self.__report_status
        self.__report_status = ReportStatus.SUCCESS
        return response

    def get_meta(self) -> dict:
        return {"name": "DummyReport", "place": "inmemory", "path": None}

    def download(self, fileHandler: BytesIO):
        fileHandler.write(b"Hello\nI'm a Dummy report!")



class DummyReportEngine(ReportEngine):
    def get_templates(self) -> List[str]:
        return ["DummyTemplate"]

    def generate_report(self, project: Project, template: str) -> Report:
        return DummyReport()
