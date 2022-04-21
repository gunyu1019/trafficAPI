from typing import Dict, Any, List
from app.utils import get_int


class BusRoute:
    def __init__(
            self,
            bus_id: int,
            bus_name: str,
            bus_type: int,
            bus_type_name: str = None,
            region: str = None,
            district: int = None,
            order: int = None
    ):
        self.id = bus_id
        self.name = bus_name
        self.type = bus_type
        self.type_name = bus_type_name
        self.region = region
        self.district = district
        self.order = order

    @classmethod
    def from_gyeonggi(cls, payload: Dict[str, Any]):
        return cls(
            bus_id=payload['routeId'],
            bus_name=payload['routeName'],
            bus_type=get_int(payload['routeTypeCd']),
            bus_type_name=payload['routeTypeName'],
            district=get_int(payload['districtCd']),
            region=payload.get('regionName'),
            order=get_int(payload['staOrder'])
        )

    @classmethod
    def from_incheon(cls, payload: Dict[str, Any]):
        bus_type_name = ["정보 없음", "지선", "간선", "좌석", "광역", "리무진", "마을버스", "순환형", "급행간선", "지선(순환)"]
        bus_type = get_int(payload['ROUTETPCD'])
        return cls(
            bus_id=payload['ROUTEID'],
            bus_name=payload['ROUTENO'],
            bus_type=bus_type,
            bus_type_name=bus_type_name[bus_type],
            order=int(payload['PATHSEQ'])
        )

    @classmethod
    def from_korea(cls, payload: Dict[str, Any], bus_type: Dict[str, int]):
        bus_type_name = payload['routetp']
        return cls(
            bus_id=payload['routeid'],
            bus_name=payload['routeno'],
            bus_type=bus_type.get(bus_type_name),
            bus_type_name=bus_type_name
        )

    @classmethod
    def from_ulsan(cls, payload: Dict[str, Any]):
        bus_type_name = {11: "광역", 12: "좌석", 13: "일반", 20: "마을", 30: "간선"}
        bus_type = payload['type']
        return cls(
            bus_id=payload['routeid'],
            bus_name=payload['routeno'],
            bus_type=bus_type,
            bus_type_name=bus_type_name[bus_type]
        )
