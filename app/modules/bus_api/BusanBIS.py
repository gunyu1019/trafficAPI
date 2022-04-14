from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusStationAround import BusStationAround
from app.modules.errors import *
from app.utils import get_list_from_ordered_dict


class BusanBIS(BaseClient):
    def __init__(self, token: str):
        super().__init__("http://apis.data.go.kr")
        self.token = token

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
        }
        return super(BusanBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_station(self, name: str):
        data = self.get(
            path="/6260000/BusanBIMS/busStopList",
            params={
                "bstopnm": name
            }
        )
        result = data['response']

        # HEAD AND BODY
        head = result['header']
        body = result['body']['items']
        if body is None:
            raise EmptyData()

        item_list = body['item']
        return [BusStation.from_busan(x) for x in get_list_from_ordered_dict(item_list)]
