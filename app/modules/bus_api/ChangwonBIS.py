import pandas
import xmltodict
import os

from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusStationAround import BusStationAround
from .models.BusanArrival import BusanBusArrival
from app.directory import directory
from app.modules.errors import *
from app.utils import haversine


class ChangwonBIS(BaseClient):
    def __init__(self, token: str, arrival_token: str):
        super().__init__("http://openapi.changwon.go.kr")
        self.token = token

        with open(
                os.path.join(directory, "data", "changwon_busstop.xml"),
                "r", encoding='utf8'
        ) as fp:
            self._station_data = xmltodict.parse(fp.read())

    def request(self, **kwargs):
        params = {
            'serviceKey': self.token
        }
        return super(ChangwonBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    def _get_data(self):
        rows = []
        for station in self._station_data['ServiceResult']['MsgBody']['StationList']['row']:
            name = station.get("STATION_NM")
            if station.get("STATION_SUB_NM", None) is not None and station.get("STATION_SUB_NM", None) != "null":
                name += "({})".format(station.get("STATION_SUB_NM"))
            rows.append({
                "id": station.get("STATION_ID"),
                "name": name,
                "posX": station.get("LOCAL_X"),
                "posY": station.get("LOCAL_Y"),
                "displayId": station.get("MOBI_NUM")
            })
        return pandas.DataFrame(rows, columns=['id', 'name', 'posX', 'posY', 'displayId'])

    def get_station(self, name: str):
        data = self._get_data()
        result = data[data['name'].str.contains(name)].to_dict('records')
        return [BusStation.from_changwon(x) for x in result]

    def get_station_around(
            self,
            pos_x: float,
            pos_y: float,
            radius: int = 500
    ):
        data = self._get_data().to_dict('records')
        result = []
        for station in data:
            station['distance'] = haversine(station['posX'], station['posY'], pos_x, pos_y)
            if station['distance'] < radius:
                result.append(
                    BusStationAround.from_changwon(station)
                )
        return result

    def get_arrival(self, station_id: int):
        return []
