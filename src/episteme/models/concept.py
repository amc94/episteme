from dataclasses import dataclass

@dataclass
class Concept:
    name: str
    known: bool = False
    note: str = ""