from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Attack:

    attack_type: List[str]
    weapon: str
    target: str
    target_type: str
    target_sub_type: str
    summary: str

    def to_dict(self) -> dict:
        return asdict(self)