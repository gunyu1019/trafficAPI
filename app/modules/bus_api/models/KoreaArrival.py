from app.utils import get_int


class KoreaBusArrival:
    def __init__(self, payload: dict):
        self.prev_count = get_int(payload.get("arrprevstationcnt"))
        self.time = get_int(payload.get("arrtime"))
        self.bus_id = get_int(payload.get("routeid"))
        self.bus_type = get_int(payload.get("routetp"))
        self.low_bus = payload.get("vehicletp", "일반버스") == "저상버스"

    @classmethod
    def empty(cls):
        return cls({})
