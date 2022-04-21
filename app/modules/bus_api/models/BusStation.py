from typing import Union, List, Dict, Any
from app.utils import get_float, get_int


class BusStation:
    def __init__(
            self,
            station_id1: Union[str, int],
            station_id2: Union[str, List[str]],
            name: str,
            st_type: Union[str, int],
            pos_x: float = None,
            pos_y: float = None,
            center: bool = None,
            region: str = None,
            district: int = None
    ):
        self.name = name
        self.id1 = self.id = station_id1
        self.id1s = [str(self.id1)]
        self.id2 = station_id2
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.type = st_type
        self.center = center
        self._region = region
        self.district = district

    @classmethod
    def from_seoul(cls, payload: Dict[str, Any]):
        pos_x = payload.get('tmX')
        pos_y = payload.get('tmY')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        return cls(
            name=payload['stNm'],
            station_id1=int(payload['stId']),
            station_id2=payload['arsId'],
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="SEOUL"
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
            district=payload.get("districtCd")
        )

    @classmethod
    def from_incheon(
            cls,
            payload: Dict[str, Any],
            _=None
    ):
        pos_x = payload.get('POSX')
        pos_y = payload.get('POSY')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        return cls(
            name=payload['BSTOPNM'],
            station_id1=int(payload['BSTOPID']),
            station_id2=payload.get('SHORT_BSTOPID', 0),
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="INCHEON",
            center=bool(payload.get('CENTERLANEYN', 0)),
            region=payload.get('ADMINNM')
        )

    @classmethod
    def from_busan(cls, payload: Dict[str, Any]):
        return cls(
            name=payload['bstopnm'],
            station_id1=get_int(payload['bstopid']),
            station_id2=payload.get('arsno'),
            pos_x=get_float(payload.get('gpsx')),
            pos_y=get_float(payload.get('gpsy')),
            st_type="BUSAN"
        )

    @classmethod
    def from_ulsan(cls, payload: Dict[str, Any]):
        return cls(
            name=payload['name'],
            station_id1=get_int(payload['id']),
            station_id2=payload.get('displayId', '0'),
            pos_x=get_float(payload.get('posX')),
            pos_y=get_float(payload.get('posY')),
            st_type="ULSAN"
        )

    @classmethod
    def from_korea(cls, payload: Dict[str, Any], city_code: int):
        return cls(
            name=payload['nodenm'],
            station_id1=payload['nodeid'],
            station_id2=str(payload.get('nodeno')),
            pos_x=get_float(payload.get('gpslong')),
            pos_y=get_float(payload.get('gpslati')),
            st_type=city_code
        )

    @classmethod
    def from_changwon(cls, payload: Dict[str, Any]):
        return cls(
            name=payload['name'],
            station_id1=payload['id'],
            station_id2=payload.get('displayId'),
            pos_x=get_float(payload.get('posX')),
            pos_y=get_float(payload.get('posY')),
            st_type="CHANGWON"
        )

    def to_data(self) -> dict:
        if self.type == "SEOUL":
            final_id = self.id2
        else:
            final_id = self.id1

        if isinstance(final_id, list):
            final_id = final_id[0]

        result = {
            "name": self.name,
            "id": final_id,
            "type": (
                ["SEOUL", "GYEONGGI", "INCHEON", "BUSAN", "CHANGWON", "ULSAN"].index(self.type) + 11
                if isinstance(self.type, str)
                else self.type
            ),
            "stationId": self.id1,
            "displayId": self.id2 if self.id2 != 0 else None,
            "posX": self.pos_x,
            "posY": self.pos_y,
        }
        if final_id == -2:
            result['ids'] = ",".join(self.id1s)
        if self.id1 == -2:
            result['stationId'] = self.id1s

        return result
