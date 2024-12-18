from dataclasses import dataclass, asdict


@dataclass
class Casualties:

    killed: int
    wound: int

    def to_dict(self) -> dict:
        return asdict(self)