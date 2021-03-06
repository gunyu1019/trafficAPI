import math
from typing import Dict, Any, Optional, Tuple
from app.utils import get_int, get_float, haversine


class RideBike:
    def __init__(self, payload: dict):
        self.rests = get_int(payload.get("parkingBikeTotCnt"))
        self.parking = get_int(payload.get("rackTotCnt"))
        self.name = payload.get("stationName")
        self.shared = get_int(payload.get("shared"))
        self.pos_x = get_float(payload.get("stationLongitude"))
        self.pos_y = get_float(payload.get("stationLatitude"))
        self.id = payload.get("stationId")

        self._distance = None
        self._position = None

    def distance_set(self, pos_x, pos_y) -> Optional[float]:
        self._position = (pos_x, pos_y)
        self._distance = haversine(
            self.pos_y, self.pos_x, pos_y, pos_x
        )
        return self._distance

    @property
    def distance(self) -> Optional[float]:
        if self._distance is None:
            return
        return round(self._distance, 2)

    @property
    def direction(self) -> Optional[int]:
        if self._position is None:
            return
        pos_x = self._position[0] - self.pos_x
        pos_y = self._position[1] - self.pos_y
        return int(
            round(math.atan2(pos_x, pos_y) * 180 / math.pi)
        )

    @classmethod
    def from_dict(cls, payload: dict):
        return cls({
            "parkingBikeTotCnt": payload.get("rests"),
            "rackTotCnt": payload.get("parking"),
            "stationName": payload.get("name"),
            "shared": payload.get("shared"),
            "stationLongitude": payload.get("posX"),
            "stationLatitude": payload.get("posY"),
            "stationId": payload.get("id")
        })

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "id": self.id,
            "name": self.name,
            "rests": self.rests,
            "parking": self.parking,
            "shared": self.shared,
            "posX": self.pos_x,
            "posY": self.pos_y
        }
        if self._position is not None:
            result['distance'] = self.distance
            result['direction'] = self.direction
        return result
