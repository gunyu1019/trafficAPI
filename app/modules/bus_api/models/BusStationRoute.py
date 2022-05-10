from typing import Union, List, Dict, Any

from .BusStation import BusStation
from app.utils import get_int


class BusStationRoute(BusStation):
    def __init__(
            self,
            station_id1: Union[str, int],
            station_id2: Union[str, List[str]],
            name: str,
            st_type: Union[str, int],
            index: int,
            direction: int,
            section_distance: int = None,
            section_speed: int = None,
            pos_x: float = None,
            pos_y: float = None,
            center: bool = None,
            region: str = None,
            district: int = None,
            roundabout: bool = False
    ):
        super(BusStationRoute, self).__init__(
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
        self.index = index
        self.direction = direction
        self.roundabout = roundabout
        self.section_distance = section_distance
        self.section_speed = section_speed

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
            station_id1=int(payload['station']),
            station_id2=payload['arsId'],
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="SEOUL",
            index=int(payload["seq"]),
            direction=get_int(payload.get("directionId", 0)),
            roundabout=(True if payload.get('transYn', 'N') == 'Y' else False),
            section_distance=get_int(payload.get("fullSectDist")),
            section_speed=get_int(payload.get("sectSpd"))
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
            index=payload["stationSeq"],
            direction=get_int(payload.get("direction", 0)),
            roundabout=(True if payload.get('turnYn', 'N') == 'Y' else False),
        )

    @classmethod
    def from_incheon(
            cls,
            payload: Dict[str, Any],
            **kwargs
    ):
        pos_x = payload.get('LNG')
        pos_y = payload.get('LAT')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        station_id = int(payload['BSTOPID'])
        direction = get_int(payload.get("DIRCD", 0))
        if direction == 2:
            direction = 0
        return cls(
            name=payload['BSTOPNM'],
            station_id1=station_id,
            station_id2=payload.get('SHORT_BSTOPID', 0),
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="INCHEON",
            region=payload.get('ADMINNM'),
            index=payload["BSTOPSEQ"],
            direction=direction,
            roundabout=bool(payload.get("roundabout", False)),
        )

    def to_dict(self) -> Dict[str, Any]:
        response = super().to_dict()
        response['index'] = self.index
        response['direction'] = self.direction
        response['roundabout'] = self.roundabout
        response['sectionDistance'] = self.section_distance
        response['sectionSpeed'] = self.section_speed
        return response
