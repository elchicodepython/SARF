from typing import List
from dataclasses import dataclass, field
from ..vulnerabilities.base import Vulnerability


@dataclass
class Report:
    uuid: str
    name: str
    project: str
    vulnerabilities: List[Vulnerability] = field(default_factory=list)

    def __str__(self):
        return self.name
