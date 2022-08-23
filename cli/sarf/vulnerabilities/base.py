from dataclasses import dataclass


@dataclass(frozen=True)
class Vulnerability:
    uuid: str
    title: str
    cvss: float
    description: str
    impact: str
    tlp: str
    references: str

    def __str__(self):
        return self.title

@dataclass(frozen=True)
class VulnerabilityTemplate(Vulnerability):
    lang: str
    author: str

    def __str__(self):
        return self.title
