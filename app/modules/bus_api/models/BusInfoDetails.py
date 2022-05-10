from datetime import datetime
from typing import Union, Dict, Any

from .BusInfo import BusInfo
from app.utils import get_int


class BusInfoDetails(BusInfo):
    def __init__(
            self,
            route_id: int,
            name: str,
            route_type: str,
            st_type: Union[str, int],
            departure: str,
            destination: str,
            first_time: datetime,
            last_time: datetime,
            term: int = None,
            min_term: int = None,
            max_term: int = None,
            region: str = None,
            district: int = None,
            departure_id: int = None,
            destination_id: int = None
    ):
        super(BusInfoDetails, self).__init__(
            route_id=route_id,
            name=name,
            route_type=route_type,
            st_type=st_type,
            region=region,
            district=district
        )
        self.min_term = min_term
        self.max_term = max_term
        self.term = term or int((min_term + max_term) / 2)
        self.departure = departure
        self.destination = destination
        self.departure_id = departure_id
        self.destination_id = destination_id
        self.first_time = first_time
        self.last_time = last_time

    @classmethod
    def from_seoul(cls, payload: Dict[str, Any]):
        bus_type = get_int(payload.get("routeType"))
        first_time = payload.get("firstBusTm")
        last_time = payload.get("lastBusTm")
        return cls(
            route_id=payload.get("busRouteId"),
            name=payload.get("busRouteNm"),
            route_type="11" + format(bus_type, '02d'),
            st_type="SEOUL",
            departure=payload.get("stStationNm"),
            destination=payload.get("edStationNm"),
            term=get_int(payload.get("term")),
            first_time=datetime.strptime(first_time, "%Y%m%d%H%M%S"),
            last_time=datetime.strptime(last_time, "%Y%m%d%H%M%S"),
        )

    @classmethod
    def from_gyeonggi(cls, payload: Dict[str, Any]):
        bus_type = get_int(payload.get("routeTypeCd"))
        first_time = payload.get("upFirstTime", "00:00")
        last_time = payload.get("upLastTime", "00:00")
        now = datetime.now().strftime("%Y%m%d")
        return cls(
            route_id=payload.get("routeId"),
            name=payload.get("routeName"),
            route_type="12" + format(bus_type, '02d'),
            st_type="GYEONGGI",
            region=payload.get("regionName"),
            district=get_int(payload.get("districtCd")),
            departure=payload.get("startStationName"),
            departure_id=get_int(payload.get("startStationId")),
            destination=payload.get("endStationName"),
            destination_id=get_int(payload.get("endStationId")),
            first_time=datetime.strptime(f"{now}-{first_time}", "%Y%m%d-%H:%M"),
            last_time=datetime.strptime(f"{now}-{last_time}", "%Y%m%d-%H:%M"),
            min_term=get_int(payload.get("peekAlloc")),
            max_term=get_int(payload.get("nPeekAlloc"))
        )

    @classmethod
    def from_incheon(cls, payload: Dict[str, Any]):
        bus_type = get_int(payload.get("ROUTETPCD"))
        first_time = payload.get("FBUS_DEPHMS", "0000")
        last_time = payload.get("LBUS_DEPHMS", "0000")
        now = datetime.now().strftime("%Y%m%d")
        return cls(
            route_id=payload.get("ROUTEID"),
            name=payload.get("ROUTENO"),
            route_type="13" + format(bus_type, '02d'),
            st_type="INCHEON",
            region=payload.get("ADMINNM"),
            departure=payload.get("ORIGIN_BSTOPNM"),
            departure_id=get_int(payload.get("ORIGIN_BSTOPID")),
            destination=payload.get("DEST_BSTOPNM"),
            destination_id=get_int(payload.get("DEST_BSTOPID")),
            first_time=datetime.strptime(f"{now}-{first_time}", "%Y%m%d-%H%M"),
            last_time=datetime.strptime(f"{now}-{last_time}", "%Y%m%d-%H%M"),
            min_term=get_int(payload.get("MIN_ALLOCGAP")),
            max_term=get_int(payload.get("MAX_ALLOCGAP"))
        )

    def to_dict(self) -> Dict[str, Any]:
        response = super().to_dict()
        response["minTerm"] = self.min_term
        response["maxTerm"] = self.max_term
        response["term"] = self.term
        response["departure"] = self.departure
        response["destination"] = self.destination
        response["departureId"] = self.departure_id
        response["destinationId"] = self.destination_id
        response["firstTime"] = None
        response["lastTime"] = None
        if self.first_time is not None:
            response["firstTime"] = self.first_time.timestamp()
        if self.last_time is not None:
            response["lastTime"] = self.last_time.timestamp()
        return response
