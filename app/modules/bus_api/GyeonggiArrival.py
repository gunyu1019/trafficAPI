from .BaseClient import BaseClient
from .models.GyeonggiArrival import GyeonggiBusArrival
from .errors import *
from app.utils import get_list_from_ordered_dict


class GyeonggiArrival(BaseClient):
    def __init__(self, token: str):
        super().__init__("http://apis.data.go.kr")
        self.token = token

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
        }
        return super(GyeonggiArrival, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_arrival(self, station_id: str):
        data = self.get(
            path="/6410000/busarrivalservice/getBusArrivalList",
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

        item_list = body['busArrivalList']
        return [GyeonggiBusArrival(x) for x in get_list_from_ordered_dict(item_list)]
