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
        self.subways = kwargs['subways'].split(',')
        self.heading = kwargs['heading']
        self.past_station = get_int(kwargs['past_station'])
        self.rapid = bool(kwargs['rapid'])

        self.prev_station = kwargs['prev_station']
        self.now_station = kwargs['now_station']
        self.post_station = kwargs['post_station']
        self.stations = kwargs['stations'].split(',')
        self.destination = kwargs['destination']
        self.destination_id = kwargs['destination_id']

        self.direction_name = kwargs['direction_name']
        self.direction = kwargs['direction']
        self.time = get_int(kwargs['time'])

        self.train_type = kwargs['train_type']
        self.train_number = kwargs['train_number']
        self._status = kwargs['status']

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        ord_key = payload.get('ordkey')
        compiler = re.compile(
            r'(?P<direction>[0-1]\d{0})(?P<order>[0-9]\d)(?P<past_station>\d{2,4})(?P<destination>[가-힣]+)(?P<rapid>\d)'
        )
        post_ord_key = compiler.search(ord_key)
        if post_ord_key is None:
            raise Exception("Unknown Regex")
        converted_post_ord_key = OrdKey(**post_ord_key.groupdict())
        return cls(
            subway=get_int(payload['subwayId']),
            direction_name=payload.get('updnLine'),
            direction=converted_post_ord_key.direction,
            destination=payload.get("bstatnNm") or converted_post_ord_key.destination,
            destination_id=payload.get("bstatnId"),
            past_station=converted_post_ord_key.past_station,
            rapid=converted_post_ord_key.rapid or payload.get("btrainSttus") is not None,
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
