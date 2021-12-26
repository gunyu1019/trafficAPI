import re


class CityList:
    def __init__(self, payload: dict):
        self.name = payload.get('cityname')
        self.id = payload.get('citycode')

    def __str__(self) -> str:
        return self.name


class BusStation:
    def __init__(
            self,
            station_id1: str,
            name: str,
            st_type: str,
            station_id2: int,
            pos_x: float = None,
            pos_y: float = None
    ):
        self.name = name
        self.id1 = self.id = station_id1
        self.id2 = station_id2
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.type = st_type

    @classmethod
    def from_korea(cls, payload: dict):
        pos_x = payload.get('gpslong')
        pos_y = payload.get('gpslati')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        return cls(
            name=payload['nodenm'],
            station_id1=payload['nodeid'],
            station_id2=int(payload['nodeno']),
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="KOREA"
        )

    @classmethod
    def from_seoul(cls, payload: dict):
        pos_x = payload.get('tmX')
        pos_y = payload.get('tmY')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        return cls(
            name=payload['stNm'],
            station_id1=int(payload['stId']),
            station_id2=int(payload['arsId']),
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="SEOUL"
        )

    def to_data(self) -> dict:
        final_id = self.id1
        if self.type == "SEOUL":
            final_id = self.id2
        return {
            "name": self.name,
            "id": final_id,
            "stationId": self.id1,
            "displayId": self.id2,
            "posX": self.pos_x,
            "posY": self.pos_y,
        }


class KoreaBusArrival:
    def __init__(self, payload: dict):
        self.station_name = payload['nodenm']
        self.station_id = payload['nodeid']

        self.time = payload.get('arrtime')
        self.name = payload.get('routeno')
        self.id = payload.get('routeid')
        self.prev_count = payload.get('arrprevstationcnt')
        self.bus_type = payload.get('routetp')
        self.vehicle_type = payload.get('vehicletp')


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

        self.time1 = payload.get('traTime1')
        self.time2 = payload.get('traTime2')
        self.vehicle_id1 = payload.get('vehId1')
        self.vehicle_id2 = payload.get('vehId2')
        self.name = payload.get('rtNm')
        self.section = payload.get('sectNm')
        self.id = payload.get('busRouteId')
        # self.prev_count = payload.get('arrprevstationcnt')
        self.bus_type = payload.get('routeType')
        self.vehicle_type1 = payload.get('busType1')
        self.vehicle_type2 = payload.get('busType2')
        self.now_station1 = payload.get('stationNm1')
        self.now_station2 = payload.get('stationNm2')

        self.is_arrive1 = bool(payload.get('isArrive1', 0))
        self.is_arrive2 = bool(payload.get('isArrive2', 0))
        self.is_full1 = bool(payload.get('isFullFlag1', 0))
        self.is_full2 = bool(payload.get('isFullFlag2', 0))
        self.is_last1 = bool(payload.get('isLast1', 0))
        self.is_last2 = bool(payload.get('isLast2', 0))
        self.last_time = bool(payload.get('lastTm', 0))  # HHMM

        self._detour = payload.get('deTourAt')
        self.detour = None
        if self._detour == '11':
            self.detour = True
        elif self._detour == '00':
            self.detour = False

    @property
    def prev_count1(self):
        regex = re.compile('\[\d번째 전\]')
        result = regex.findall(self.msg1)
        if len(result) > 0:
            return result[0].lstrip('[').rstrip('번째 전]')
        return 0

    @property
    def prev_count2(self):
        regex = re.compile('\[\d번째 전\]')
        result = regex.findall(self.msg2)
        if len(result) > 0:
            return result[0].lstrip('[').rstrip('번째 전]')
        return 0
