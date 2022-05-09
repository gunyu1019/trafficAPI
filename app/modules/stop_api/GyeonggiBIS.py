from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusStationAround import BusStationAround
from .models.GyeonggiArrival import GyeonggiBusArrival
from app.modules.errors import *
from app.utils import get_list_from_ordered_dict


class GyeonggiBIS(BaseClient):
    def __init__(self, token: str, arrival_token: str = None):
        super().__init__("http://apis.data.go.kr")
        self.token = token
        self.arrival_token = arrival_token or token

    def request(self, arrival_token: bool = False, **kwargs):
        params = {
            'serviceKey': self.token if not arrival_token else self.arrival_token
        }
        return super(GyeonggiBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_station(self, name: str):
        data = self.get(
            path="/6410000/busstationservice/getBusStationList",
            params={
                "keyword": name
            }
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
            }
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
            }
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
            arrival_token=True
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busArrivalList']
        return [GyeonggiBusArrival(x) for x in get_list_from_ordered_dict(item_list)]