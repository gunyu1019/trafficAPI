from .BaseClient import BaseClient
from .models.IncheonArrival import IncheonBusArrival
from .errors import *
from app.utils import get_list_from_ordered_dict


class IncheonArrival(BaseClient):
    def __init__(self, token: str):
        super().__init__("http://apis.data.go.kr")
        self.token = token

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
        }
        return super(IncheonArrival, self).request(_default_params=params, _default_xml=True, **kwargs)

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
            }
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        head = result['msgHeader']
        body = result['msgBody']
        if body is None:
            raise EmptyData()
        item_list = body['itemList']
        return [IncheonBusArrival(x) for x in get_list_from_ordered_dict(item_list)]
