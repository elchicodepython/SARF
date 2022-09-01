from dataclasses import dataclass


@dataclass(frozen=True)
class Report:
    uuid: str
    name: str
    project: str

    def __str__(self):
        return self.name
