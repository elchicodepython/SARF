from typing import Optional
from os import environ


def get_report_id() -> Optional[str]:
    return environ.get("SARF_REPORT")


def get_report_id_or_print_error() -> Optional[str]:
    report_id = get_report_id()
    if not report_id:
        print("SARF_REPORT enviromental variable is required.")
    return report_id
