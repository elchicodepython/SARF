from ..base import Report
from ...vulnerabilities.base import Vulnerability


class ReportUseCases:
    def __init__(
        self,
        reports_crud,
    ):
        self.__reports_crud = reports_crud

    def get_report(self, uuid: str) -> Report:
        rows = self.__reports_crud.where([{"field": "uuid", "op": "=", "value": uuid}])
        if row_list := list(rows):
            return row_list[0]

    def add_vuln(self, report_uuid: str, vuln: Vulnerability):
        report = self.get_report(report_uuid)
        if report:
            self.__reports_crud.update(
                [
                    {"field": "uuid", "op": "=", "value": report_uuid}
                ],
                {
                    "vulnerabilities": report.vulnerabilities + [vuln]
                }
            )
            self.__reports_crud.commit()
            return True
        return False
