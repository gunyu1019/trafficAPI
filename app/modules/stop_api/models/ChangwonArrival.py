from app.utils import get_int


class ChangwonBusArrival:
    def __init__(self, payload: dict):
        self.status = payload.get("CALC_DATE") != "null"
        self.id = payload['ROUTE_ID']
        self.index = payload['STATION_ORD']

        self.time = None
        self.prev_count = None
        self.vehicle_id = None
        if self.status:
            self.time = get_int(payload.get('PREDICT_TRAV_TM'))
            self.prev_count = get_int(payload.get('LEFT_STATION'))
            self.vehicle_id = get_int(payload.get('ARRV_VH_ID'))

    @classmethod
    def empty(cls):
        return cls({})
