from typing import Union, List, Dict, Any, Optional
from app.utils import get_int, get_float


class BusVehicle:
    def __init__(
            self,
            car_number: str,
            index: int,
            route_id: int,
            station_id: str,
            is_last: Optional[bool] = False,
            is_full: Optional[bool] = None,
            is_arrive: Optional[bool] = None,
            vehicle_type: int = 0,
            seat: Optional[int] = None,
            congestion: Optional[int] = None,
            section_distance: Optional[float] = None
    ):
        self.car_number = car_number
        self.index = index
        self.route_id = route_id
        self.station_id = station_id
        self.is_last = is_last
        self.is_full = is_full
        self.is_arrival = is_arrive
        self.type = vehicle_type
        self.seat = seat
        self.congestion = congestion
        self.section_distance = section_distance

    @staticmethod
    def convert_seat(people: int) -> Optional[int]:
        if people == -1:
            return None
        return people

    @staticmethod
    def convert_incheon(data: int) -> Optional[int]:
        if data == 255:
            return None
        return data

    @classmethod
    def from_seoul(cls, payload: Dict[str, Any]):
        print(payload)
        congestion = get_int(payload.get('congetion'))
        if congestion > 0:
            congestion -= 2
        section_distance = get_float(payload['sectDist'])
        full_section_distance = get_float(payload['fullSectDist'])
        return cls(
            car_number=payload.get('plainNo'),
            index=int(payload['sectOrd']),
            route_id=payload['sectionId'],
            station_id=payload['lastStnId'],
            is_last=bool(int(payload.get('islastyn', 0))),
            is_full=bool(int(payload.get('isFullFlag', False))),
            is_arrive=bool(int(payload.get('stopFlag', False))),
            vehicle_type=int(payload['busType']),
            congestion=congestion,
            section_distance=round(section_distance / full_section_distance * 100, 3),
        )

    @classmethod
    def from_gyeonggi(cls, payload: Dict[str, Any]):
        seat = cls.convert_seat(payload.get("remainSeatCnt", -1))
        return cls(
            car_number=payload.get('plateNo'),
            index=int(payload['stationSeq']),
            route_id=payload['routeId'],
            station_id=payload['stationId'],
            is_last=bool(int(payload.get('endBus', 0))),
            is_full=True if seat == 0 else False,
            seat=seat,
            vehicle_type=int(payload['lowPlate'])
        )

    @classmethod
    def from_incheon(cls, payload: Dict[str, Any]):
        seat = cls.convert_incheon(int(payload.get("REMAIND_SEAT", 255)))
        congestion = cls.convert_incheon(int(payload.get("CONGESTION", 255)))
        return cls(
            car_number=payload.get('BUS_NUM_PLATE'),
            index=int(payload['LATEST_STOPSEQ']),
            route_id=payload['ROUTEID'],
            station_id=payload['LATEST_STOP_ID'],
            is_last=bool(int(payload.get('LASTBUSYN', 0))),
            is_full=True if seat == 0 else False,
            seat=seat,
            congestion=congestion,
            vehicle_type=int(payload['LOW_TP_CD'])
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "congestion": self.congestion,
            "carNumber": self.car_number,
            "lowBus": bool(self.type),
            "index": self.index,
            "station": self.station_id,
            "routeId": self.route_id,
            "seat": self.seat,
            "isLast": self.is_last,
            "isFull": self.is_full,
            "isArrival": self.is_arrival,
            "sectionDistance": self.section_distance
        }
