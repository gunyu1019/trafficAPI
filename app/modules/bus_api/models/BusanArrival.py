from .BusStation import BusStation
from app.utils import get_int


class BusanBusArrival:
    def __init__(self, payload: dict):
        payload['bstopnm'] = payload.get('nodenm')
        self.station = BusStation.from_busan(payload)

        self.name = payload['lineno']
        self.id = payload['lineid']
        self.index = payload['bstopidx']
        self.car_number1 = payload.get('carno1')
        self.car_number2 = payload.get('carno2')
        self.time1 = get_int(payload.get('min1'))
        self.time2 = get_int(payload.get('min2'))
        self.prev_count1 = get_int(payload.get('station1'))
        self.prev_count2 = get_int(payload.get('station2'))
        self.low_bus1 = bool(payload.get('lowplate1', False))
        self.low_bus2 = bool(payload.get('lowplate2', False))
        self.seat1 = get_int(payload.get('seat1', -1))
        self.seat2 = get_int(payload.get('seat2', -1))
        self.type_name = payload['bustype']

    @classmethod
    def empty(cls):
        return cls({})

    @property
    def type(self) -> int:
        bus_type_name = [("급행버스", "심야버스(급행)"), ("좌석버스", "좌석버스(좌석)"), ("일반버스", "심야버스(일반)"), "마을버스"]
        for index, name in enumerate(bus_type_name):
            if self.type_name in name:
                return index
        return 9

    @property
    def is_night(self) -> bool:
        return self.type_name.startswith("심야버스")
