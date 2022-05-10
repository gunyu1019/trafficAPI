from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusInfo import BusInfo
from .models.BusInfoDetails import BusInfoDetails
from .models.BusVehicle import BusVehicle
from .models.BusStationRoute import BusStationRoute
from .models.BusStationAround import BusStationAround
from .models.IncheonArrival import IncheonBusArrival
from app.modules.errors import *
from app.utils import get_list_from_ordered_dict


class IncheonBIS(BaseClient):
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
        return super(IncheonBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_station(
            self,
            name: str,
            rows: int = 10,
            page: int = 1
    ):
        data = self.get(
            path="/6280000/busStationService/getBusStationNmList",
            params={
                "bstopNm": name,
                "numOfRows": rows,
                "pageNo": page
            },
            token=self.token
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return [BusStation.from_incheon(x) for x in get_list_from_ordered_dict(item_list)]

    def get_station_around(
            self,
            pos_x: float,
            pos_y: float,
            rows: int = 10,
            page: int = 1
    ):
        data = self.get(
            path="/6280000/busStationService/getBusStationAroundList",
            params={
                "LAT": pos_x,
                "LNG": pos_y,
                "numOfRows": rows,
                "pageNo": page
            },
            token=self.token
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return [BusStationAround.from_incheon(x, self) for x in get_list_from_ordered_dict(item_list)]

    def get_station_id(
            self,
            station_id: int,
            rows: int = 10,
            page: int = 1
    ):
        data = self.get(
            path="/6280000/busStationService/getBusStationIdList",
            params={
                "bstopId": station_id,
                "numOfRows": rows,
                "pageNo": page
            },
            token=self.token
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return [BusStation.from_incheon(x) for x in get_list_from_ordered_dict(item_list)]

    def get_route(
            self,
            station_id: str,
            rows: int = 10,
            page: int = 1
    ):
        data = self.get(
            path="/6280000/busStationService/getBusStationViaRouteList",
            params={
                "bstopId": station_id,
                "numOfRows": rows,
                "pageNo": page
            },
            token=self.token
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return [BusRoute.from_incheon(x) for x in get_list_from_ordered_dict(item_list)]

    def get_arrival(
            self,
            station_id: str,
            rows: int = 100,
            page: int = 1
    ):
        data = self.get(
            path="/6280000/busArrivalService/getAllRouteBusArrivalList",
            params={
                "bstopId": station_id,
                "numOfRows": rows,
                "pageNo": page
            },
            token=self.arrival_token
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return [IncheonBusArrival(x) for x in get_list_from_ordered_dict(item_list)]

    def get_bus(
            self,
            name: str,
            rows: int = 100,
            page: int = 1
    ):
        data = self.get(
            path="/6280000/busRouteService/getBusRouteNo",
            params={
                "routeNo": name,
                "numOfRows": rows,
                "pageNo": page
            },
            token=self.bus_token
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return [BusInfo.from_incheon(x) for x in get_list_from_ordered_dict(item_list)]

    def get_bus_detail(
            self,
            bus_id: str,
            rows: int = 100,
            page: int = 1
    ):
        data = self.get(
            path="/6280000/busRouteService/getBusRouteId",
            params={
                "routeId": bus_id,
                "numOfRows": rows,
                "pageNo": page
            },
            token=self.bus_token
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return BusInfoDetails.from_incheon(item_list)

    def get_bus_route(
            self,
            bus_id: str,
            rows: int = 100,
            page: int = 1
    ):
        data = self.get(
            path="/6280000/busRouteService/getBusRouteSectionList",
            params={
                "routeId": bus_id,
                "numOfRows": rows,
                "pageNo": page
            },
            token=self.bus_token
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = get_list_from_ordered_dict(body['itemList'])

        result = []
        direction = item_list[0]['DIRCD']
        for index, bus_route in enumerate(item_list):
            if index + 1 < len(item_list):
                if item_list[index + 1]['DIRCD'] != direction:
                    bus_route['roundabout'] = True
                    direction = item_list[index + 1]['DIRCD']
                else:
                    bus_route['roundabout'] = False
            result.append(
                BusStationRoute.from_incheon(bus_route)
            )
        return result

    def get_bus_location(
            self,
            bus_id: str,
            rows: int = 100,
            page: int = 1
    ):
        data = self.get(
            path="/6280000/busLocationService/getBusRouteLocation",
            params={
                "routeId": bus_id,
                "numOfRows": rows,
                "pageNo": page
            },
            token=self.location_token
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return [BusVehicle.from_incheon(x) for x in get_list_from_ordered_dict(item_list)]
