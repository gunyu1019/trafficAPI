from .BaseClient import BaseClient
from .models import *
from .errors import *
from ..utils import get_list_from_ordered_dict


class GyeonggiBIS(BaseClient):
    def __init__(self, token: str):
        super().__init__("http://apis.data.go.kr")
        self.token = token

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
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
        head = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busStationList']
        return [BusStation.from_gyeonggi(x) for x in get_list_from_ordered_dict(item_list)]

    def get_route(self, station_id: str):
        data = self.get(
            path="/6410000/busstationservice/getBusStationViaRouteList",
            params={
                "stationId": station_id
            }
        )
        result = data['response']

        # HEAD AND BODY
        head = result['msgHeader']
        if 'msgBody' not in result:
            raise EmptyData()
        body = result['msgBody']

        item_list = body['busRouteList']
        return [BusRoute.from_gyeonggi(x) for x in get_list_from_ordered_dict(item_list)]
