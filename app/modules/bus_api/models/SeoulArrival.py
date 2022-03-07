import re
from app.utils import get_int
from .BusStation import BusStation


class SeoulBusArrival:
    def __init__(self, payload: dict):
        station_name = payload['stNm']
        station_id1 = payload['stId']
        station_id2 = payload['arsId']
        station_type = payload['stationTp']
        pos_x = payload.get('gpsX')
        pos_y = payload.get('gpsY')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        self.station = BusStation(
            name=station_name,
            station_id1=station_id1,
            station_id2=station_id2,
            st_type=station_type,
            pos_x=pos_x,
            pos_y=pos_y
        )

        self.next_station = payload['nxtStn']
        self.term = payload['term']

        self.direction = payload['adirection']
        self.msg1 = payload['arrmsg1']
        self.msg2 = payload['arrmsg2']
        self.msg1_detail = payload['arrmsgSec1']
        self.msg2_detail = payload['arrmsgSec2']

        self.time1 = get_int(payload.get('traTime1'))
        self.time2 = get_int(payload.get('traTime2'))
        self.vehicle_id1 = payload.get('vehId1')
        self.vehicle_id2 = payload.get('vehId2')
        self.name = payload.get('rtNm')
        self.section = payload.get('sectNm')
        self.id = payload.get('busRouteId')

        self.bus_type = get_int(payload.get('routeType'))
        self.vehicle_type1 = get_int(payload.get('busType1'))
        self.vehicle_type2 = get_int(payload.get('busType2'))
        self.now_station1 = payload.get('stationNm1')
        self.now_station2 = payload.get('stationNm2')

        self.is_arrive1 = bool(get_int(payload.get('isArrive1', 0)))
        self.is_arrive2 = bool(get_int(payload.get('isArrive2', 0)))
        self.is_full1 = bool(get_int(payload.get('isFullFlag1', 0)))
        self.is_full2 = bool(get_int(payload.get('isFullFlag2', 0)))
        self.is_last1 = bool(get_int(payload.get('isLast1', 0)))
        self.is_last2 = bool(get_int(payload.get('isLast2', 0)))
        self.last_time = bool(get_int(payload.get('lastTm', 0)))  # HHMM

        self._detour = payload.get('deTourAt')
        self.detour = None
        if self._detour == '11':
            self.detour = True
        elif self._detour == '00':
            self.detour = False

    @property
    def prev_count1(self):
        regex = re.compile('\[\d*번째 전]')
        result = regex.findall(self.msg1)
        if len(result) > 0:
            return get_int(result[0].lstrip('[').rstrip('번째 전]'))
        return 0

    @property
    def prev_count2(self):
        regex = re.compile('\[\d*번째 전]')
        result = regex.findall(self.msg2)
        if len(result) > 0:
            return get_int(result[0].lstrip('[').rstrip('번째 전]'))
        return 0
