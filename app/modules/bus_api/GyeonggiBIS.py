from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusStationAround import BusStationAround
from .models.BusStationRoute import BusStationRoute
from .models.BusInfo import BusInfo
from .models.BusInfoDetails import BusInfoDetails
from .models.BusVehicle import BusVehicle
from .models.GyeonggiArrival import GyeonggiBusArrival
from app.modules.errors import *
from app.utils import get_list_from_ordered_dict


class GyeonggiBIS(BaseClient):
    def __init__(
            self,
            token: str = None,
            arrival_token: str = None,
            bus_token: str = None,
            location_token: str = None
    ):
        super().__init__("http://apis.data.go.kr")
        self.token = token
        self.arrival_token = arrival_token or token
        self.bus_token = bus_token
        self.location_token = location_token or bus_token

    def request(self, token: str, **kwargs):
        params = {
            'serviceKey': token
        }
        return super(GyeonggiBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_station(self, name: str):
        data = self.get(
            path="/6410000/busstationservice/getBusStationList",
            params={
                "keyword": name
            },
            token=self.token
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busStationList']
        return [BusStation.from_gyeonggi(x) for x in get_list_from_ordered_dict(item_list)]

    def get_station_around(
            self,
            pos_x: float,
            pos_y: float
    ):
        data = self.get(
            path="/6410000/busstationservice/getBusStationAroundList",
            params={
                "x": pos_x,
                "y": pos_y
            },
            token=self.token
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busStationAroundList']
        return [BusStationAround.from_gyeonggi(x) for x in get_list_from_ordered_dict(item_list)]

    def get_route(self, station_id: str):
        data = self.get(
            path="/6410000/busstationservice/getBusStationViaRouteList",
            params={
                "stationId": station_id
            },
            token=self.token
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busRouteList']
        return [BusRoute.from_gyeonggi(x) for x in get_list_from_ordered_dict(item_list)]

    def get_arrival(self, station_id: str):
        data = self.get(
            path="/6410000/busarrivalservice/getBusArrivalList",
            params={
                "stationId": station_id
            },
            token=self.arrival_token
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busArrivalList']
        return [GyeonggiBusArrival(x) for x in get_list_from_ordered_dict(item_list)]

    def get_bus(self, name: str):
        data = self.get(
            path="/6410000/busrouteservice/getBusRouteList",
            params={
                "keyword": name
            },
            token=self.bus_token
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busRouteList']
        return [BusInfo.from_seoul(x) for x in get_list_from_ordered_dict(item_list)]

    def get_bus_details(self, bus_id: str):
        data = self.get(
            path="/6410000/busrouteservice/getBusRouteInfoItem",
            params={
                "routeId": bus_id
            },
            token=self.bus_token
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busRouteInfoItem']
        return [BusInfoDetails.from_gyeonggi(x) for x in get_list_from_ordered_dict(item_list)]

    def get_bus_route(self, bus_id: str):
        data = self.get(
            path="/6410000/busrouteservice/getBusRouteStationList",
            params={
                "routeId": bus_id
            },
            token=self.bus_token
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busRouteStationList']
        return [BusStationRoute.from_gyeonggi(x) for x in get_list_from_ordered_dict(item_list)]

    def get_bus_location(self, bus_id: str):
        data = self.get(
            path="/6410000/buslocationservice/getBusLocationList",
            params={
                "routeId": bus_id
            },
            token=self.location_token
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busLocationList']
        return [BusVehicle.from_gyeonggi(x) for x in get_list_from_ordered_dict(item_list)]
