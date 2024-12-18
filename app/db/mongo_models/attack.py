from dataclasses import dataclass, asdict


@dataclass
class Attack:

    attack_type: str
    attack_type_2: str
    attack_type_3: str
    weapon: str
    target: str
    target_type: str
    target_sub_type: str
    summary: str

    def to_dict(self) -> dict:
        return asdict(self)