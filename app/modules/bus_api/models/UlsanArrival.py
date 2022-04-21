from app.utils import get_int


class UlsanBusArrival:
    def __init__(self, payload: dict):
        self.prev_count = get_int(payload.get("PREVSTOPCNT"))
        self.time = get_int(payload.get("ARRIVALTIME"))
        self.bus_id = get_int(payload.get("ROUTEID"))
        self.car_number = payload.get("VEHICLENO")
        self.bus_name = payload.get("ROUTENM")

    @classmethod
    def empty(cls):
        return cls({})
