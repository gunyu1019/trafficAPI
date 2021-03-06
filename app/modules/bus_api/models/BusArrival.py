from typing import List, Optional, Dict, Any
from .BusRoute import BusRoute
from .BusanArrival import BusanBusArrival
from .ChangwonArrival import ChangwonBusArrival
from .SeoulArrival import SeoulBusArrival
from .GyeonggiArrival import GyeonggiBusArrival
from .KoreaArrival import KoreaBusArrival
from .IncheonArrival import IncheonBusArrival
from .UlsanArrival import UlsanBusArrival


class BusRouteInfo:
    def __init__(self, **payload):
        self.name: str = payload['name']
        self.id: str = payload['id']
        self.type: str = payload['type']
        self.is_end: bool = payload.get('is_end')
        self.is_wait: bool = payload.get('is_wait')
        self.arrival_info: List[BusArrivalInfo] = [
            BusArrivalInfo(**x) for x in payload['arrival_info']
        ]

    @classmethod
    def from_seoul(cls, data: SeoulBusArrival, version: str = 'v1'):
        return cls(
            name=data.name,
            id=data.id,
            type="11" + format(data.bus_type, '02d') if version == 'v2' else "10" + format(data.bus_type, '02d'),
            is_end="운행종료" == data.msg1,
            is_wait="출발대기" == data.msg1 and "회차대기" == data.msg1,
            arrival_info=[
                {
                    "type": getattr(data, "vehicle_type{0}".format(key)),
                    "time": getattr(data, "time{0}".format(key)),
                    "prev_count": getattr(data, "prev_count{0}".format(key)),
                    "prev_station": getattr(data, "now_station{0}".format(key)),
                    "is_full": getattr(data, "is_full{0}".format(key)),
                    "is_arrival": getattr(data, "is_arrive{0}".format(key)),
                    "is_last": getattr(data, "is_last{0}".format(key))
                } for key in range(1, 3) if (
                    "운행종료" != getattr(data, "msg{0}".format(key)) and
                    "출발대기" != getattr(data, "msg{0}".format(key)) and
                    "회차대기" != getattr(data, "msg{0}".format(key))
                )
            ]
        )

    @classmethod
    def from_gyeonggi(cls, route: BusRoute, arrival: Optional[GyeonggiBusArrival] = None, version: str = 'v1'):
        flag = getattr(arrival, "flag", None)
        return cls(
            name=route.name,
            id=route.id,
            type="12" + format(route.type, '02d') if version == 'v2' else "20" + format(route.type, '02d'),
            is_end="STOP" == flag,
            is_wait="WAIT" == flag,
            arrival_info=[
                {
                    "car_number": getattr(arrival, "car_number{0}".format(key), None),
                    "type": getattr(arrival, "vehicle_type{0}".format(key), None),
                    "time": (
                        getattr(arrival, "time{0}".format(key), None) * 60
                        if getattr(arrival, "time{0}".format(key), None) is not None
                        else None
                    ),
                    "seat": cls.convert_seat(
                        getattr(arrival, "seat{0}".format(key), None)
                    ),
                    "prev_count": getattr(arrival, "prev_count{0}".format(key), None),
                    "is_full": True if getattr(arrival, "is_full{0}".format(key), None) == 0 else False
                } for key in range(1, 3) if arrival is not None
            ]
        )

    @classmethod
    def from_incheon(cls, route: BusRoute, arrival: List[IncheonBusArrival], version: str = 'v1'):
        new_cls = cls(
            name=route.name,
            id=route.id,
            type="13" + format(route.type, '02d') if version == 'v2' else "30" + format(route.bus_type, '02d'),
            arrival_info=[]
        )
        new_cls.arrival_info = [
            BusArrivalInfo(**{
                "car_number": x.car_number,
                "congestion": x.congestion,
                "type": int(x.low_bus),
                "time": x.time,
                "seat": x.seat,
                "prev_count": x.prev_count,
                "prev_station": x.now_station,
                "is_full": True if x.seat == 0 else False,
                "is_last": x.is_last
            }) for x in arrival
        ]
        return new_cls

    @classmethod
    def from_busan(cls, data: BusanBusArrival):
        return cls(
            name=data.name,
            id=data.id,
            type="21" + format(data.type, '02d'),
            arrival_info=[
                {
                    "car_number": getattr(data, "car_number{0}".format(key), None),
                    "seat": cls.convert_seat(
                        getattr(data, "seat{0}".format(key), None)
                    ),
                    "type": getattr(data, "low_bus{0}".format(key)),
                    "time": (
                        getattr(data, "time{0}".format(key), None) * 60
                        if getattr(data, "time{0}".format(key), None) is not None
                        else None
                    ),
                    "prev_count": getattr(data, "prev_count{0}".format(key), 0),
                    "lowBus": getattr(data, "low_bus{0}".format(key), 0)
                } for key in range(1, 3) if getattr(data, "prev_count{0}".format(key), None) is not None
            ]
        )

    @classmethod
    def from_changwon(cls, data: ChangwonBusArrival, route: Dict[str, Any], route_type: int):
        return cls(
            name=route['name'],
            id=data.id,
            type="24" + format(route_type, '02d'),
            arrival_info=[
                {
                    "type": None,
                    "time": data.time,
                    "prev_count": data.prev_count,
                }
            ] if data.status else []
        )

    @classmethod
    def from_korea(cls, route: BusRoute, arrival: List[KoreaBusArrival], type_prefix: int):
        new_cls = cls(
            name=route.name,
            id=route.id,
            type=str(type_prefix) + format(route.type, '02d'),
            arrival_info=[]
        )
        new_cls.arrival_info = [
            BusArrivalInfo(**{
                "type": int(x.low_bus),
                "time": x.time,
                "prev_count": x.prev_count,
            }) for x in arrival
        ]
        return new_cls

    @classmethod
    def from_ulsan(cls, route: BusRoute, arrival: List[UlsanBusArrival]):
        new_cls = cls(
            name=route.name,
            id=route.id,
            type="25" + format(route.type, '02d'),
            arrival_info=[]
        )
        new_cls.arrival_info = [
            BusArrivalInfo(**{
                "type": None,
                "time": x.time,
                "prev_count": x.prev_count,
                "car_number": x.car_number,
            }) for x in arrival
        ]
        return new_cls

    @staticmethod
    def convert_seat(people: int) -> Optional[int]:
        if people == -1:
            return None
        return people

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "id": self.id,
            "type": self.type,
            "isEnd": self.is_end,
            "isWait": self.is_wait,
            "arrivalInfo": [x.to_dict() for x in self.arrival_info]
        }


class BusArrivalInfo:
    def __init__(self, **payload):
        self.type: int = payload['type']
        self.prev_count: int = payload['prev_count']
        self.time: int = payload['time']
        self.seat: Optional[int] = payload.get('seat')
        self.prev_station: Optional[str] = payload.get('prev_station')
        self.congestion: Optional[int] = payload.get('congestion')
        self.car_number: Optional[str] = payload.get('car_number')
        self.is_full: Optional[bool] = payload.get('is_full')
        self.is_last: Optional[bool] = payload.get('is_last')
        self.is_arrival: Optional[bool] = payload.get('is_arrival')

    def to_dict(self) -> dict:
        return {
            "congestion": self.congestion,
            "carNumber": self.car_number,
            "lowBus": bool(self.type),
            "time": self.time,
            "seat": self.seat,
            "isFull": self.is_full,
            "isArrival": self.is_arrival,
            "isLast": self.is_last,
            "prevCount": self.prev_count
        }
