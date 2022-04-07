from typing import Any, Dict, Optional


class Station:
    def __init__(self, payload: Dict[str, Any]):
        self.station_id = payload.get("STATION_CD")
        self.name = payload.get("STATION_NM")
        self.code = payload.get("FR_CODE")

        self.line_number = payload.get("LINE_NUM")
        self._subway = None
        self._arrival_station = None

    @property
    def subway(self):
        if self._subway is None:
            return
        return self._subway.name

    @property
    def arrival_subway(self) -> Optional[int]:
        if self._subway is None:
            return
        return int(self._subway.subwayId)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "arrivalSubwayId": self.arrival_subway,
            "arrivalStationId": self._arrival_station,
            "code": self.code,
            "name": self.name,
            "subway": self.subway,
            "stationId": self.station_id
        }
