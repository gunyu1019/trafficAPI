from typing import Any, Dict


class Timetable:
    def __init__(self, **kwargs):
        self.code = kwargs['code']
        self.destination = kwargs['name']
        self.direction = kwargs['direction']
        self.id = kwargs['station_id']
        self.name = kwargs['name']
        self.week_type = kwargs['week_type']
        self._time = kwargs['time']

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        return cls(
            destination=payload['SUBWAYENAME'],
            direction=int(payload['INOUT_TAG']),
            code=payload['FR_CODE'],
            station_id=payload['STATION_CD'],
            name=payload['STATION_NM'],
            time=payload['LEFTTIME'],
            week_type=int(payload['WEEK_TAG'])
        )

    @property
    def hours(self) -> int:
        return int(self._time.split(":")[0])

    @property
    def minutes(self) -> int:
        return int(self._time.split(":")[1])

    @property
    def seconds(self) -> int:
        return int(self._time.split(":")[2])

    def to_dict(self):
        return {
            "destination": self.destination,
            "direction": self.direction,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds,
            "name": self.name,
            "id": self.id,
            "week_type": self.week_type
        }
