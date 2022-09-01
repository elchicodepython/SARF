from dataclasses import dataclass


@dataclass(frozen=True)
class Vulnerability:
    uuid: str
    title: str
    cvss: float
    description: str
    impact: str
    tlp: str
    evidences: str
    references: str

    def __str__(self):
        return self.title


@dataclass(frozen=True)
class VulnerabilityTemplate:
    uuid: str
    title: str
    cvss: float
    description: str
    impact: str
    tlp: str
    references: str
    lang: str
    author: str

    def __str__(self):
        return f"[{self.lang.upper()}] {self.title}"
