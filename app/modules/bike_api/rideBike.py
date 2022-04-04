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

    def distance_set(self, pos_x, pos_y) -> Optional[float]:
        self._distance = haversine(
            self.pos_y, self.pos_x, pos_y, pos_x
        )
        return self._distance

    @property
    def distance(self) -> Optional[float]:
        if self._distance is None:
            return
        return round(self._distance, 2)

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
        if self.distance is not None:
            result['distance'] = self.distance
        return result
