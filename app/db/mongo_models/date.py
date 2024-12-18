from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Date:

    day: int
    month: int
    year: int
    full_date: datetime

    def to_dict(self) -> dict:
        return asdict(self)