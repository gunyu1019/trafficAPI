from typing import Union, List, Dict, Any
from app.utils import get_float, get_int, optional_int_to_str


class BusInfo:
    def __init__(
            self,
            route_id: int,
            name: str,
            route_type: str,
            st_type: Union[str, int],
            region: str = None,
            district: int = None
    ):
        self.name = name
        self.id = route_id
        self.type = route_type
        self.st_type = st_type
        self._region = region
        self.district = district

    @classmethod
    def from_seoul(cls, payload: Dict[str, Any]):
        bus_type = get_int(payload.get("routeType"))
        return cls(
            route_id=payload.get("busRouteId"),
            name=payload.get("busRouteNm"),
            route_type="11" + format(bus_type, '02d'),
            st_type="SEOUL",
        )

    @classmethod
    def from_gyeonggi(cls, payload: Dict[str, Any]):
        bus_type = get_int(payload.get("routeTypeCd"))
        return cls(
            route_id=payload.get("routeId"),
            name=payload.get("routeName"),
            route_type="12" + format(bus_type, '02d'),
            st_type="GYEONGGI",
            region=payload.get("regionName"),
            district=get_int(payload.get("districtCd"))
        )

    @classmethod
    def from_incheon(cls, payload: Dict[str, Any]):
        bus_type = get_int(payload.get("ROUTETPCD"))
        return cls(
            route_id=payload.get("ROUTEID"),
            name=payload.get("ROUTENO"),
            route_type="13" + format(bus_type, '02d'),
            st_type="INCHEON",
            region=payload.get("ADMINNM")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "id": self.id
        }
