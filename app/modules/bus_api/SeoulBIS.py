from app.modules.baseClient import BaseClient
from .models.SeoulArrival import SeoulBusArrival
from .models.BusStation import BusStation
from .models.BusStationAround import BusStationAround
from .models.BusStationRoute import BusStationRoute
from .models.BusInfo import BusInfo
from .models.BusInfoDetails import BusInfoDetails
from .models.BusVehicle import BusVehicle
from app.modules.errors import *
from app.utils import get_list_from_ordered_dict


class SeoulBIS(BaseClient):
    def __init__(
            self,
            token: str = None,
            bus_token: str = None,
            location_token: str = None
    ):
        super().__init__("http://ws.bus.go.kr")
        self.token = token
        self.bus_token = bus_token
        self.location_token = location_token

    async def request(self, token: str, **kwargs):
        params = {
            'serviceKey': token
        }
        return await super(SeoulBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    async def get_station(self, name: str):
        data = await self.get(
            path="/api/rest/stationinfo/getStationByName",
            params={
                "stSrch": name
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
        return [BusStation.from_seoul(x) for x in get_list_from_ordered_dict(item_list)]

    async def get_station_around(
            self,
            pos_x: float,
            pos_y: float,
            around: int = 500
    ):
        data = await self.get(
            path="/api/rest/stationinfo/getStationByPos",
            params={
                "tmX": pos_x,
                "tmY": pos_y,
                "radius": around
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
        return [BusStationAround.from_seoul(x) for x in get_list_from_ordered_dict(item_list)]

    async def get_arrival(self, station_id: int):
        data = await self.get(
            path="/api/rest/stationinfo/getStationByUid",
            params={
                "arsId": station_id
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
        return [SeoulBusArrival(x) for x in get_list_from_ordered_dict(item_list)]

    async def get_bus(self, name: str):
        data = await self.get(
            path="/api/rest/busRouteInfo/getBusRouteList",
            params={
                "strSrch": name
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
        return [BusInfo.from_seoul(x) for x in get_list_from_ordered_dict(item_list)]

    async def get_bus_detail(self, bus_id: str):
        data = await self.get(
            path="/api/rest/busRouteInfo/getRouteInfo",
            params={
                "busRouteId": bus_id
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
        return BusInfoDetails.from_seoul(item_list)

    async def get_bus_route(self, bus_id: str):
        data = await self.get(
            path="/api/rest/busRouteInfo/getStaionByRoute",
            params={
                "busRouteId": bus_id
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

        result = []
        direction = 0
        pre_direction = ""
        for bus_route in get_list_from_ordered_dict(item_list):
            if pre_direction != bus_route['direction']:
                direction += 1
            bus_route['directionId'] = direction
            result.append(
                BusStationRoute.from_seoul(bus_route)
            )
        return result

    async def get_bus_location(self, bus_id: str):
        data = await self.get(
            path="/api/rest/buspos/getBusPosByRtid",
            params={
                "busRouteId": bus_id
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
        return [BusVehicle.from_seoul(x) for x in get_list_from_ordered_dict(item_list)]
