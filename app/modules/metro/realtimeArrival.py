import re
from typing import Dict, Any, NamedTuple, Literal
from app.utils import get_int


class OrdKey(NamedTuple):
    direction: Literal[0, 1]
    order: int
    past_station: int
    destination: str
    rapid: Literal[0, 1]


class RealtimeArrival:
    def __init__(self, **kwargs):
        self.subway = kwargs['subway']
        self.subways = [int(x) for x in kwargs['subways'].split(',')]
        self.heading = kwargs['heading']
        self.past_station = get_int(kwargs['past_station'])
        self.rapid = bool(kwargs['rapid'])

        self.station = kwargs['now_station']
        self.prev_station = kwargs['prev_station']
        self.post_station = kwargs['post_station']
        self.stations = kwargs['stations'].split(',')
        self.destination = kwargs['destination']
        self.destination_id = kwargs['destination_id']

        self.direction_name = kwargs['direction_name']
        self.direction = int(kwargs['direction'])
        self.time = get_int(kwargs['time'])

        self.train_type = kwargs['train_type']
        self.train_number = kwargs['train_number']
        self._status = kwargs['status']

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        ord_key = payload.get('ordkey')
        compiler = re.compile(
            r'(?P<direction>[0-1]\d{0})'
            r'(?P<order>[0-9]\d{0})'
            r'(?P<past_station>\d{1,4})'
            r'(?P<destination>[가-힣|()0-9]+)'
            r'(?P<rapid>\d)'
        )
        post_ord_key = compiler.search(ord_key)
        if post_ord_key is None:
            raise Exception("Unknown Regex, {}".format(ord_key))
        converted_post_ord_key = OrdKey(**post_ord_key.groupdict())
        return cls(
            subway=get_int(payload['subwayId']),
            direction_name=payload.get('updnLine'),
            direction=converted_post_ord_key.direction,
            destination=payload.get("bstatnNm") or converted_post_ord_key.destination,
            destination_id=payload.get("bstatnId"),
            past_station=converted_post_ord_key.past_station,
            rapid=converted_post_ord_key.rapid and payload.get("btrainSttus") is not None,
            heading=payload.get('subwayHeading'),
            train_type=payload.get("btrainSttus"),
            train_number=payload.get("btrainNo"),
            time=get_int(payload.get("barvlDt")),
            status=payload.get("arvlCd"),
            prev_station=payload.get("statnFid"),
            post_station=payload.get("statnTid"),
            now_station=payload.get("statnId"),
            stations=payload.get("statnList", ""),
            subways=payload.get("subwayList", "")
        )

    @property
    def is_entry(self) -> bool:
        return self._status == "0"

    @property
    def is_arrive(self) -> bool:
        return self._status == "1"

    @property
    def is_departure(self) -> bool:
        return self._status == "2"

    @property
    def is_prev_departure(self) -> bool:
        return self._status == "3"

    @property
    def is_prev_entry(self) -> bool:
        return self._status == "4"

    @property
    def is_prev_arrive(self) -> bool:
        return self._status == "5"

    def to_dict(self, add_subway: bool = False) -> Dict[str, Any]:
        result = {
            "direction": self.direction,
            "direction_name": self.direction_name,
            "destination": self.destination,
            "stationId": self.station,
            "heading": self.heading,
            "isRapid": self.rapid,
            "isArrive": self.is_arrive,
            "isEntry": self.is_entry,
            "isDeparture": self.is_departure,
            "isPrevArrive": self.is_prev_arrive,
            "isPrevEntry": self.is_prev_entry,
            "isPrevDeparture": self.is_prev_departure,
            "rapidInfo": self.train_type,
            "train": self.train_number,
            # "transfer": self.subways,
            # "transferStation": self.stations,
            "time": self.time,
            "prevCount": self.past_station,
            "prevStation": self.prev_station,
            "nextStation": self.post_station
        }
        if add_subway:
            result["subway"] = self.subway
        return result
