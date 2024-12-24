from dataclasses import dataclass, asdict


@dataclass
class Location:
    country: str
    region: str
    city: str
    latitude: float
    longitude: float
    province: str
    exact_location: str

    def to_dict(self) -> dict:
        return asdict(self)