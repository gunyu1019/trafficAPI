from app.modules.baseClient import BaseClient
from .models.SeoulArrival import SeoulBusArrival
from .models.BusStation import BusStation
from .models.BusStationAround import BusStationAround
from app.modules.errors import *
from app.utils import get_list_from_ordered_dict


class SeoulBIS(BaseClient):
    def __init__(
            self,
            token: str
    ):
        super().__init__("http://ws.bus.go.kr")
        self.token = token

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
        }
        return super(SeoulBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_station(self, name: str):
        data = self.get(
            path="/api/rest/stationinfo/getStationByName",
            params={
                "stSrch": name
            }
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        head = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()

        item_list = body['itemList']
        return [BusStation.from_seoul(x) for x in get_list_from_ordered_dict(item_list)]

    def get_station_around(
            self,
            pos_x: float,
            pos_y: float,
            around: int = 500
    ):
        data = self.get(
            path="/api/rest/stationinfo/getStationByPos",
            params={
                "tmX": pos_x,
                "tmY": pos_y,
                "radius": around
            }
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        head = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()

        item_list = body['itemList']
        return [BusStationAround.from_seoul(x) for x in get_list_from_ordered_dict(item_list)]

    def get_arrival(self, station_id: int):
        data = self.get(
            path="/api/rest/stationinfo/getStationByUid",
            params={
                "arsId": station_id
            }
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        head = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()

        item_list = body['itemList']
        return [SeoulBusArrival(x) for x in get_list_from_ordered_dict(item_list)]
