from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusStationAround import BusStationAround
from .models.IncheonArrival import IncheonBusArrival
from app.modules.errors import *
from app.utils import get_list_from_ordered_dict


class IncheonBIS(BaseClient):
    def __init__(self, token: str, arrival_token: str = None):
        super().__init__("http://apis.data.go.kr")
        self.token = token
        self.arrival_token = arrival_token or token

    def request(self, arrival_token: bool = False, **kwargs):
        params = {
            'serviceKey': self.token if not arrival_token else self.arrival_token
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
            }
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
            }
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
            }
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
            }
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
            arrival_token=True
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return [IncheonBusArrival(x) for x in get_list_from_ordered_dict(item_list)]
