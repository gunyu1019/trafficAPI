import pandas
import xmltodict
import os
from urllib import parse

from app.modules.baseClient import BaseClient
from .models.BusStation import BusStation
from .models.BusRoute import BusRoute
from .models.BusStationAround import BusStationAround
from .models.ChangwonArrival import ChangwonBusArrival
from app.directory import directory
from app.modules.errors import *
from app.utils import haversine, get_list_from_ordered_dict


class ChangwonBIS(BaseClient):
    def __init__(self, token: str, arrival_token: str = None):
        super().__init__("http://openapi.changwon.go.kr")
        self.token = token
        self.arrival_token = arrival_token or token

        with open(
                os.path.join(directory, "data", "changwon_busstop.xml"),
                "r", encoding='utf8'
        ) as fp:
            self._station_data = xmltodict.parse(fp.read())
        with open(
                os.path.join(directory, "data", "changwon_bus.xml"),
                "r", encoding='utf8'
        ) as fp:
            self._bus_data = xmltodict.parse(fp.read())

    def request(self, arrival_token: bool = False, **kwargs):
        params = {
            'serviceKey': self.token if not arrival_token else self.arrival_token
        }
        return super(ChangwonBIS, self).request(_default_params=params, _default_xml=True, **kwargs)

    def get_station_data(self):
        rows = []
        for station in self._station_data['ServiceResult']['MsgBody']['StationList']['row']:
            name = station.get("STATION_NM")
            if station.get("STATION_SUB_NM", None) is not None and station.get("STATION_SUB_NM", None) != "null":
                name += "({})".format(station.get("STATION_SUB_NM"))
            rows.append({
                "id": station.get("STATION_ID"),
                "name": name,
                "posX": float(station.get("LOCAL_X")),
                "posY": float(station.get("LOCAL_Y")),
                "displayId": station.get("MOBI_NUM")
            })
        return pandas.DataFrame(rows, columns=['id', 'name', 'posX', 'posY', 'displayId'])

    def get_bus_data(self):
        rows = []
        for station in self._bus_data['ServiceResult']['MsgBody']['BusList']['row']:
            rows.append({
                "id": station.get("ROUTE_ID"),
                "displayName": station.get("ROUTE_NM"),
                "departure": station.get("ORGT_STATION_ID"),
                "destination": station.get("DST_STATION_ID"),
                "name": station.get("ROUTE_NUM"),
                "stationCount": station.get("STATION_CNT"),
                "length": station.get("ROUTE_LEN"),
                "color": station.get("ROUTE_COLOR"),
                "firstTime": station.get("FIRST_TM"),
                "lastTime": station.get("LAST_TM")
            })
        return pandas.DataFrame(
            rows,
            columns=[
                'id',
                'displayName',
                'departure',
                'destination',
                'name',
                'stationCount',
                'length',
                'color',
                'firstTime',
                'lastTime'
            ])

    def get_station(self, name: str):
        data = self.get_station_data()
        result = data[data['name'].str.contains(name)].to_dict('records')
        return [BusStation.from_changwon(x) for x in result]

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
                    BusStationAround.from_changwon(station)
                )
        return result

    def get_arrival(self, station_id: int):
        data = self.get(
            path="/rest/bis/BusArrives/",
            params={
                "station": station_id
            },
            arrival_token=True
        )
        result = data['ServiceResult']

        # HEAD AND BODY
        _ = result['MsgHeader']
        body = result['MsgBody']['ArriveInfoList']
        if body is None:
            raise EmptyData()

        item_list = body['row']
        return [ChangwonBusArrival(x) for x in get_list_from_ordered_dict(item_list)]

    def update_update(self):
        data = self.get(
            path="/rest/bis/Station/",
            converted=False
        )
        with open(
            os.path.join(directory, "data", "changwon_busstop.xml"), "w", encoding='utf8'
        ) as file:
            file.write(data)

    def update_bus_info(self):
        data = self.get(
            path="/rest/bis/Bus",
            converted=False
        )
        with open(
            os.path.join(directory, "data", "changwon_bus.xml"), "w", encoding='utf8'
        ) as file:
            file.write(data)
