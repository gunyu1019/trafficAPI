from typing import Literal
from app.utils import get_int


class GyeonggiBusArrival:
    def __init__(self, payload: dict):
        self.flag: Literal["RUN" "PASS", "STOP", "WAIT"] = payload.get('flag')
        self.bus_id = payload.get('routeId')
        self.station_id = payload.get('stationId')

        self.prev_count1 = get_int(payload.get('locationNo1'))
        self.time1 = get_int(payload.get('predictTime1'))
        self.vehicle_type1 = get_int(payload.get('lowPlate1'))
        self.car_number1 = payload.get('plateNo1')
        self.seat1: int = get_int(payload.get('remainSeatCnt1'))

        self.prev_count2 = get_int(payload.get('locationNo2'))
        self.time2 = get_int(payload.get('predictTime2'))
        self.vehicle_type2 = get_int(payload.get('lowPlate2'))
        self.car_number2 = payload.get('plateNo2')
        self.seat2: int = get_int(payload.get('remainSeatCnt2'))
        self.order = payload.get("staOrder")

    @classmethod
    def empty(cls):
        return cls({})
