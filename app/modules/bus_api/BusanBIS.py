import os
import xmltodict
import pandas

from app.directory import directory
from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusStationAround import BusStationAround
from .models.BusanArrival import BusanBusArrival
from app.modules.errors import *
from app.utils import get_list_from_ordered_dict, haversine


class BusanBIS(BaseClient):
    def __init__(self, token: str):
        super().__init__("http://apis.data.go.kr")
        self.token = token

        with open(
                os.path.join(directory, "data", "busan_busstop.xml"),
                "r", encoding='utf8'
        ) as fp:
            self._station_data = xmltodict.parse(fp.read())

    def get_station_data(self):
        rows = []
        for station in self._station_data['response']['body']['items']['item']:
            rows.append({
                "bstopid": station.get("bstopid"),
                "bstopnm": station.get("bstopnm"),
                "arsno": station.get("arsno"),
                "gpsx": float(station.get("gpsx")),
                "gpsy": float(station.get("gpsy"))
            })
        return pandas.DataFrame(rows, columns=['bstopid', 'bstopnm', 'arsno', 'gpsx', 'gpsy'])

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
        }
        return super(BusanBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    # def get_station(self, name: str):
    #     data = self.get(
    #         path="/6260000/BusanBIMS/busStopList",
    #         params={
    #             "bstopnm": name
    #         }
    #     )
    #     result = data['response']

    #     # HEAD AND BODY
    #     _ = result['header']
    #     body = result['body']['items']
    #     if body is None:
    #         raise EmptyData()

    #     item_list = body['item']
    #     return [BusStation.from_busan(x) for x in get_list_from_ordered_dict(item_list)]

    def get_station(self, name: str):
        data = self.get_station_data()
        result = data[data['bstopnm'].str.contains(name)].to_dict('records')
        return [BusStation.from_busan(x) for x in result]

    def get_station_around(
            self,
            pos_x: float,
            pos_y: float,
            radius: int = 500
    ):
        data = self.get_station_data().to_dict('records')
        result = []
        for station in data:
            station['distance'] = haversine(station['gpsx'], station['gpsy'], pos_x, pos_y)
            if station['distance'] < radius:
                result.append(
                    BusStationAround.from_busan(station)
                )
        return result

    def get_arrival(self, station_id: int):
        data = self.get(
            path="/6260000/BusanBIMS/stopArrByBstopid",
            params={
                "bstopid": station_id
            }
        )
        result = data['response']

        # HEAD AND BODY
        _ = result['header']
        body = result['body']['items']
        if body is None:
            raise EmptyData()

        item_list = body['item']
        return [BusanBusArrival(x) for x in get_list_from_ordered_dict(item_list)]
