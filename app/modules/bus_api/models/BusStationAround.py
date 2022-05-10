from typing import Union, List, Dict, Any

from .BusStation import BusStation
from app.modules.errors import EmptyData
from app.utils import get_float, get_int


class BusStationAround(BusStation):
    def __init__(
            self,
            station_id1: Union[str, int],
            station_id2: Union[str, List[str]],
            name: str,
            st_type: Union[str, int],
            distance: int,
            pos_x: float = None,
            pos_y: float = None,
            center: bool = None,
            region: str = None,
            district: int = None
    ):
        super(BusStationAround, self).__init__(
            name=name,
            station_id1=station_id1,
            station_id2=station_id2,
            pos_x=pos_x,
            pos_y=pos_y,
            st_type=st_type,
            center=center,
            region=region,
            district=district
        )
        self.distance = distance

    @classmethod
    def from_seoul(cls, payload: Dict[str, Any]):
        pos_x = payload.get('gpsX')
        pos_y = payload.get('gpsY')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        return cls(
            name=payload['stationNm'],
            station_id1=int(payload['stationId']),
            station_id2=payload['arsId'],
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="SEOUL",
            distance=int(payload.get("dist", 0))
        )

    @classmethod
    def from_gyeonggi(cls, payload: Dict[str, Any]):
        pos_x = payload.get('x')
        pos_y = payload.get('y')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        return cls(
            name=payload['stationName'],
            station_id1=int(payload['stationId']),
            station_id2=payload.get('mobileNo', 0),
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="GYEONGGI",
            center=(True if payload.get('centerYn', 'N') == 'Y' else False),
            region=payload.get('regionName'),
            district=payload.get("districtCd"),
            distance=int(payload['distance'])
        )

    @classmethod
    def from_incheon(
            cls,
            payload: Dict[str, Any],
            client=None
    ):
        pos_x = payload.get('LNG')
        pos_y = payload.get('LAT')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        station_id = int(payload['BSTOPID'])
        try:
            station_info: BusStation = client.get_station_id(station_id=station_id)
        except (EmptyData, AttributeError):
            station_id2 = None
            center = None
            region = None
        else:
            station_id2 = station_info.id2
            center = station_info.center
            region = getattr(station_info, "_region")
        return cls(
            name=payload['BSTOPNM'],
            station_id1=station_id,
            station_id2=station_id2,
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="INCHEON",
            center=center,
            region=region,
            distance=int(payload.get("DISTANCE", 0))
        )

    @classmethod
    def from_busan(cls, payload: Dict[str, Any]):
        return cls(
            name=payload['bstopnm'],
            station_id1=get_int(payload['bstopid']),
            station_id2=payload.get('arsno'),
            pos_x=get_float(payload.get('gpsx')),
            pos_y=get_float(payload.get('gpsy')),
            st_type="BUSAN",
            distance=int(payload.get("distance", 0))
        )

    @classmethod
    def from_changwon(
            cls,
            payload: Dict[str, Any]
    ):
        return cls(
            name=payload['name'],
            station_id1=payload['id'],
            station_id2=payload.get('displayId'),
            pos_x=get_float(payload.get('posX')),
            pos_y=get_float(payload.get('posY')),
            st_type="CHANGWON",
            distance=int(payload.get("distance", 0))
        )

    @classmethod
    def from_korea(cls, payload: Dict[str, Any], city_code: int):
        return cls(
            name=payload['nodenm'],
            station_id1=payload['nodeid'],
            station_id2=str(payload.get('nodeno')),
            pos_x=get_float(payload.get('gpslong')),
            pos_y=get_float(payload.get('gpslati')),
            distance=int(payload.get("distance", 0)),
            st_type=city_code
        )

    @classmethod
    def from_ulsan(
            cls,
            payload: Dict[str, Any]
    ):
        return cls(
            name=payload['name'],
            station_id1=get_int(payload['id']),
            station_id2=payload.get('displayId', '0'),
            pos_x=get_float(payload.get('posX')),
            pos_y=get_float(payload.get('posY')),
            st_type="ULSAN",
            distance=int(payload.get("distance", 0))
        )

    def to_data(self) -> dict:
        response = super().to_data()
        response['distance'] = self.distance
        return response
