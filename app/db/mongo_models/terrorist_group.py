from dataclasses import dataclass, asdict


@dataclass
class TerroristGroup:
    name: str
    perps: int

    def to_dict(self) -> dict:
        return asdict(self)