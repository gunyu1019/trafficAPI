from typing import NamedTuple, Optional


class SubwayInfo(NamedTuple):
    subwayId: Optional[int] = None
    name: str = None
    inSubwayId: Optional[str] = None


class StationInfo(NamedTuple):
    subway: int = None
    stationId: int = None
    name: str = None
