from typing import Union


class BusStation:
    def __init__(
            self,
            station_id1: Union[str, int],
            name: str,
            st_type: str,
            station_id2: int,
            pos_x: float = None,
            pos_y: float = None,
            center: bool = None,
            region: str = None,
            district: int = None
    ):
        self.name = name
        self.id1 = self.id = station_id1
        self.id2 = station_id2
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.type = st_type
        self.center = center
        self._region = region
        self.district = district

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

    @classmethod
    def from_gyeonggi(cls, payload: dict):
        pos_x = payload.get('x')
        pos_y = payload.get('y')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        return cls(
            name=payload['stationName'],
            station_id1=int(payload['stationId']),
            station_id2=int(payload.get('mobileNo', 0)),
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="GYEONGGI",
            center=(True if payload.get('centerYn', 'N') == 'Y' else False),
            region=payload.get('regionName'),
            district=payload.get("districtCd")
        )

    @classmethod
    def from_incheon(cls, payload: dict):
        pos_x = payload.get('POSX')
        pos_y = payload.get('POSY')
        if pos_x is not None:
            pos_x = float(pos_x)
        if pos_y is not None:
            pos_y = float(pos_y)
        return cls(
            name=payload['BSTOPNM'],
            station_id1=int(payload['BSTOPID']),
            station_id2=int(payload['SHORT_BSTOPID']),
            pos_x=pos_x,
            pos_y=pos_y,
            st_type="INCHEON",
            region=payload.get('ADMINNM')
        )

    def to_data(self) -> dict:
        if self.type == "SEOUL":
            final_id = self.id2
        else:
            final_id = self.id1

        if isinstance(final_id, list):
            final_id = final_id[0]
        return {
            "name": self.name,
            "id": final_id,
            "type": ["SEOUL", "GYEONGGI", "INCHEON"].index(self.type) + 11,
            "stationId": self.id1,
            "displayId": self.id2,
            "posX": self.pos_x,
            "posY": self.pos_y,
        }