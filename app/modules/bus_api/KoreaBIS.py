from .BaseClient import BaseClient
from .models import *
from .errors import *
from ..utils import get_list_from_ordered_dict


class KoreaBIS(BaseClient):
    def __init__(self, token: str):
        super().__init__("http://openapi.tago.go.kr")
        self.token = token

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
        }
        return super(KoreaBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_city(
            self
    ):
        data = self.get(
            path="/openapi/service/BusSttnInfoInqireService/getCtyCodeList"
        )
        result = data['response']

        # HEAD AND BODY
        head = result['header']
        body = result['body']

        item_list = body['items']['item']
        if 'item' in item_list:
            item_list = item_list['item']
            return [CityList(x) for x in get_list_from_ordered_dict(item_list)]
        raise EmptyData()

    def get_station(
            self,
            city_code: int,
            name: str = None,
            station_id: int = None,
            rows: int = 10,
            page: int = 1
    ):
        data = self.get(
            path="/openapi/service/BusSttnInfoInqireService/getSttnNoList",
            params={
                "cityCode": city_code,
                "nodeNm": name,
                "nodeNo": station_id,
                "numOfRows": rows,
                "pageNo": page
            }
        )
        result = data['response']

        # HEAD AND BODY
        head = result['header']
        body = result['body']

        item_list = body['items']
        if 'item' in item_list:
            item_list = item_list['item']
            return [BusStation.from_korea(x) for x in get_list_from_ordered_dict(item_list)]
        raise EmptyData()
