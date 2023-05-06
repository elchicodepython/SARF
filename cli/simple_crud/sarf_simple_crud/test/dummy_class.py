from dataclasses import dataclass


@dataclass
class Dummy:
    id: str
    name: str
    def method(self):
        return True
