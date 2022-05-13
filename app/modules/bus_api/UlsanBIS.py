import pandas
import xmltodict
import os
from urllib import parse

from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusStationAround import BusStationAround
from .models.UlsanArrival import UlsanBusArrival
from .KoreaBIS import KoreaBIS
from app.directory import directory
from app.modules.errors import *
from app.utils import haversine, get_list_from_ordered_dict, get_float


class UlsanBIS(BaseClient):
    def __init__(self, token: str, korea_token: str = None):
        super().__init__("http://openapi.its.ulsan.kr")
        self.token = token
        self.korea_token = korea_token or token
        self.korea_client = KoreaBIS(korea_token, 26)

        with open(
                os.path.join(directory, "data", "ulsan_busstop.xml"),
                "r", encoding='utf8'
        ) as fp:
            self._station_data = xmltodict.parse(fp.read())
        with open(
                os.path.join(directory, "data", "ulsan_bus.xml"),
                "r", encoding='utf8'
        ) as fp:
            self._bus_data = xmltodict.parse(fp.read())

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
        }
        return super(UlsanBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_station_data(self):
        rows = []
        for station in self._station_data['tableInfo']['list']['row']:
            rows.append({
                "id": station.get("STOPID"),
                "name": station.get("STOPNAME"),
                "posX": get_float(station.get("STOPX")),
                "posY": get_float(station.get("STOPY")),
                "displayId": 0
            })
        return pandas.DataFrame(rows, columns=['id', 'name', 'posX', 'posY', 'displayId'])

    def get_bus_data(self):
        rows = []
        for station in self._bus_data['tableInfo']['list']['row']:
            rows.append({
                "id": station.get("BRTID"),
                "departure": station.get("STOPSTID"),
                "destination": station.get("STOPEDID"),
                "name": station.get("BRTNO"),
                "type": station.get("BRTTYPE"),
                "direction": station.get("DIRECTION"),
                "displayId": station.get("DISPLAYID")
            })
        return pandas.DataFrame(
            rows,
            columns=[
                "id", "departure", "destination", "name", "type", "direction"
            ])

    def get_station(self, name: str):
        data = self.get_station_data()
        result = data[data['name'].str.contains(name)].to_dict('records')
        return [BusStation.from_ulsan(x) for x in result]

    def get_station_around(
            self,
            pos_x: float,
            pos_y: float,
            radius: int = 500
    ):
        data = self.get_station_data().to_dict('records')
        result = []
        for station in data:
            station['distance'] = haversine(station['posX'], station['posY'], pos_x, pos_y)
            if station['distance'] < radius:
                result.append(
                    BusStationAround.from_ulsan(station)
                )
        return result

    def get_route(self, station_id: int):
        bus_ids = [str(x.id).lstrip("USB") for x in self.korea_client.get_route(
            "USB{}".format(station_id)
        )]
        result = []
        bus_data = self.get_bus_data()
        for bus_id in bus_ids:
            result += bus_data[bus_data['id'] == bus_id].to_dict("records")
        return [BusRoute.from_ulsan(x) for x in result]

    def get_arrival(self, station_id: int):
        data = self.get(
            path="/UlsanAPI/getBusArrivalInfo.xo",
            params={
                "stopid": station_id,
                "pageNo": 1,
                "numOfRows": 1000
            }
        )
        result = data['tableInfo']

        # HEAD AND BODY
        body = result['list']
        if body is None:
            raise EmptyData()

        item_list = body['row']
        return [UlsanBusArrival(x) for x in get_list_from_ordered_dict(item_list)]
