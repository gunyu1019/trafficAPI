from .BaseClient import BaseClient
from .models import *
from .errors import *
from ..utils import get_list_from_ordered_dict


class KoreaArrival(BaseClient):
    def __init__(self, token: str):
        super().__init__("http://openapi.tago.go.kr")
        self.token = token

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
        }
        return super(KoreaArrival, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_arrival(
            self,
            city_code: int,
            station_id: str,
            rows: int = 10,
            page: int = 1

    ):
        data = self.get(
            method='GET',
            path="/openapi/service/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList",
            params={
                "cityCode": city_code,
                "nodeNo": station_id,
                "numOfRows": rows,
                "pageNo": page
            }
        )
        result = data['response']

        # HEAD AND BODY
        head = result['header']
        body = result['body']

        item_list = body['items']['item']
        if 'item' in item_list:
            item_list = item_list['item']
            return [KoreaBusArrival(x) for x in get_list_from_ordered_dict(item_list)]
        raise EmptyData()

    def get_city(
            self
    ):
        data = self.get(
            path="/openapi/service/ArvlInfoInqireService/getCtyCodeList"
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
