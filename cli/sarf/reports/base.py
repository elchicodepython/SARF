from abc import ABC, abstractmethod
from enum import Enum
from typing import List
from io import BytesIO

from ..projects.base import Project


class ReportStatus(Enum):
    REQUESTED = 0
    ERROR     = 1
    SUCCESS   = 2


class Report(ABC):

    @abstractmethod
    def get_status(self) -> ReportStatus:
        pass

    @abstractmethod
    def get_meta(self) -> dict:
        pass

    @abstractmethod
    def download(self, fileHandler: BytesIO):
        pass


class ReportEngine(ABC):
    @abstractmethod
    def get_templates(self) -> List[str]:
        pass

    @abstractmethod
    def generate_report(project: Project, template: str) -> Report:
        pass
