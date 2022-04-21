from typing import Dict

from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusStationAround import BusStationAround
from .models.KoreaArrival import KoreaBusArrival
from app.modules.errors import *
from app.utils import get_list_from_ordered_dict


class KoreaBIS(BaseClient):
    def __init__(self, token: str, city_code: int, arrival_token: str = None):
        super().__init__("http://apis.data.go.kr")
        self.token = token
        self.arrival_token = arrival_token or token
        self.city_code = city_code

    def request(self, arrival_token: bool = False, **kwargs):
        params = {
            'serviceKey': self.token if not arrival_token else self.arrival_token
        }
        return super(KoreaBIS, self).request(_default_params=params, _default_xml=False, **kwargs)

    def get_station(self, name: str):
        data = self.get(
            path="/1613000/BusSttnInfoInqireService/getSttnNoList",
            params={
                "pageNo": 1,
                "numOfRows": 100,
                "nodeNm": name,
                "cityCode": self.city_code,
                "_type": "json"
            }
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['header']
        body = result['body']['items']
        if body == '' or body is None:
            raise EmptyData()

        item_list = body['item']
        return [BusStation.from_korea(x, self.city_code) for x in get_list_from_ordered_dict(item_list)]

    def get_route(self, station_id: str, bus_type: Dict[str, int] = None):
        if bus_type is None:
            bus_type = {}
        data = self.get(
            path="/1613000/BusSttnInfoInqireService/getSttnThrghRouteList",
            params={
                "pageNo": 1,
                "numOfRows": 100,
                "nodeId": station_id,
                "cityCode": self.city_code,
                "_type": "json"
            }
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['header']
        body = result['body']['items']
        if body == '' or body is None:
            raise EmptyData()

        item_list = body['item']
        return [BusRoute.from_korea(r, bus_type) for r in get_list_from_ordered_dict(item_list)]

    def get_arrival(self, station_id: int):
        data = self.get(
            path="/1613000/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList",
            params={
                "pageNo": 1,
                "numOfRows": 100,
                "nodeId": station_id,
                "cityCode": self.city_code,
                "_type": "json"
            },
            arrival_token=True
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['header']
        body = result['body']['items']
        if body == '' or body is None:
            raise EmptyData()

        item_list = body['item']
        return [KoreaBusArrival(x) for x in get_list_from_ordered_dict(item_list)]
