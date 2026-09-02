from dataclasses import dataclass, field


@dataclass
class Route:
    number: int
    start_point: str
    end_point: str
    stops: list[int | str] = field(default=lambda: [])
