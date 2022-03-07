from app.utils import get_int


class IncheonBusArrival:
    def __init__(self, payload: dict):
        self.station_id = payload.get('BSTOPID')

        self.time = get_int(payload.get('ARRIVALESTIMATETIME'))
        self.id = payload.get('ROUTEID')
        self.bus_id = payload.get('BUSID')
        self.car_number = payload.get('BUS_NUM_PLATE')
        self.prev_count = get_int(payload.get('REST_STOP_COUNT'))
        self.bus_type = payload.get('routetp')
        self.low_bus = bool(payload.get('LOW_TP_CD'))

        self.seat = None
        seat: int = get_int(payload.get('REMAIND_SEAT', 255))
        if seat != 255:
            self.seat = seat
        self.direction: int = get_int(payload.get('DIRCD'))
        self.is_last: int = get_int(payload.get('LASTBUSYN'))
        congestion: int = get_int(payload.get('CONGESTION', 255))
        self.congestion = None
        if congestion != 255:
            self.congestion = congestion
        self.now_station = payload.get('LATEST_STOP_NAME')
        self.now_station_id = payload.get('LATEST_STOP_ID')

    @classmethod
    def empty(cls):
        return cls({})
