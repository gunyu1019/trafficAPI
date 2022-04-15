import os
from collections import namedtuple
from typing import NamedTuple

import xmltodict
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.arrival import get_incheon, get_gyeonggi
from app.config.config import get_config
from app.directory import directory
from app.modules import bus_api
from app.modules.bus_api.models.BusArrival import BusRouteInfo
from app.utils import haversine

bp = Blueprint(
    name="bus_api",
    import_name="bus_api",
    url_prefix="/bus"
)


class Token(NamedTuple):
    korea_bis: str
    korea_arrival: str
    seoul_bis: str
    gyeonggi_bis: str
    gyeonggi_arrival: str
    incheon_bis: str
    incheon_arrival: str
    busan_bis: str


parser = get_config()
token = Token(
    korea_bis=parser.get("token", "KoreaBIS"),
    korea_arrival=parser.get("token", "KoreaArrival"),
    seoul_bis=parser.get("token", "SeoulBIS"),
    gyeonggi_bis=parser.get("token", "GyeonggiBIS"),
    gyeonggi_arrival=parser.get("token", "GyeonggiArrival"),
    incheon_bis=parser.get("token", "IncheonBIS"),
    incheon_arrival=parser.get("token", "IncheonArrival"),
    busan_bis=parser.get("token", "BusanBIS")
)

with open(os.path.join(directory, "data", "ulsan_data.xml"), 'r', encoding='utf8') as fp:
    ulsan_data = xmltodict.parse(fp.read())

with open(os.path.join(directory, "data", "changwon_data.xml"), 'r', encoding='utf8') as fp:
    changwon_data = xmltodict.parse(fp.read())


@bp.route("/station", methods=['GET'])
def station_info():
    args = req.args
    if "name" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Bus Station name."
            }),
            400
        )
    station_name = args.get('name')
    city_code = args.get('cityCode', default="1")
    if city_code == "11":
        try:
            client = bus_api.SeoulBIS(token=token.seoul_bis)
            result = client.get_station(name=station_name)
        except bus_api.EmptyData:
            result = []
    elif city_code == "12":
        try:
            client = bus_api.GyeonggiBIS(token=token.seoul_bis)
            result = client.get_station(name=station_name)
        except bus_api.EmptyData:
            result = []
    elif city_code == "13":
        try:
            client = bus_api.IncheonBIS(token=token.seoul_bis)
            result = client.get_station(name=station_name)
        except bus_api.EmptyData:
            result = []
    elif city_code == "13":
        try:
            client = bus_api.IncheonBIS(token=token.seoul_bis)
            result = client.get_station(name=station_name)
        except bus_api.EmptyData:
            result = []
    elif city_code == "14":
        try:
            client = bus_api.BusanBIS(token=token.seoul_bis)
            result = client.get_station(name=station_name)
        except bus_api.EmptyData:
            result = []
    elif city_code == "1":
        client = [
            bus_api.SeoulBIS(token=token.seoul_bis),
            bus_api.GyeonggiBIS(token=token.seoul_bis),
            bus_api.IncheonBIS(token=token.seoul_bis)
        ]
        result = []
        _list_ids = []

        for _client in client:
            try:
                _result = _client.get_station(name=station_name)
            except bus_api.EmptyData:
                continue

            for index, station in enumerate(_result):
                if station.id1 in _list_ids:
                    _index = _list_ids.index(station.id1)
                    if isinstance(result[_index].id2, list):
                        if station.id2 not in result[_index].id2:
                            result[_index].id2.append(station.id2)
                    else:
                        if int(result[_index].id2) == 0:
                            result[_index].id2 = station.id2
                            result[_index].type = station.type
                        elif result[_index].id2 != station.id2 and int(station.id2) != 0:
                            result[_index].id2 = [
                                result[_index].id2, station.id2
                            ]
                else:
                    _list_ids.append(station.id1)
                    result.append(station)
    elif city_code == "3":
        client = [
            (bus_api.BusanBIS(token=token.busan_bis), None),
            (bus_api.KoreaBIS(token=token.korea_bis), 26),
            (bus_api.KoreaBIS(token=token.korea_bis), 38100),
            (bus_api.KoreaBIS(token=token.korea_bis), 38070)
        ]
        result = []
        station_list = {}

        for _client, _city_code in client:
            try:
                if _city_code is not None:
                    _result = _client.get_station(name=station_name, city_code=_city_code)
                else:
                    _result = _client.get_station(name=station_name)
            except bus_api.EmptyData:
                continue

            for station in _result:
                if station.name not in station_list:
                    station_list[station.name] = {}
                if station.type not in station_list[station.name]:
                    station_list[station.name][station.type] = []
                station_list[station.name][station.type].append(station)
        for station in station_list.values():
            if len(station.keys()) <= 1:
                for _city_code in station.values():
                    result += _city_code
                continue
            keys = list(station.keys())

            v_station = {}
            for basic_station in station[keys[0]]:
                v_station[basic_station.id] = {
                    "station": [],
                    "info": basic_station
                }

            for _city_code in keys[1:]:
                _list_id = []
                for basic_station in station[keys[0]]:
                    min_distance = 500
                    candidate = None
                    for other_station in station[_city_code]:
                        if other_station.id in _list_id:
                            continue
                        distance = haversine(
                            basic_station.pos_x, basic_station.pos_y, other_station.pos_x, other_station.pos_y
                        )
                        if distance <= min_distance:
                            min_distance = distance
                            candidate = other_station
                    if candidate is None:
                        continue
                    _list_id.append(candidate.id)
                    v_station[basic_station.id]["station"].append(candidate)

            for basic_station in v_station.keys():
                info: bus_api.BusStation = v_station[basic_station]['info']
                for other_station in v_station[basic_station]["station"]:
                    if not isinstance(info.id2, list):
                        info.id2 = [info.id2]
                    info.id2.append(other_station.id2)
                    info.id1 = -2
                    info.id1s.append(other_station.id1)
                    info.type = 99
                result.append(info)
    else:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Invalid City Code"
            }),
            400
        )
    return jsonify([
        x.to_data() for x in result if x.id != 0
    ])


@bp.route("/station/around", methods=['GET'])
def station_info_around():
    args = req.args
    if "posX" not in args or "posY" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing posX or posY."
            }),
            400
        )
    pos_x = args.get('posX', type=float)
    pos_y = args.get('posY', type=float)
    city_code = args.get('cityCode', default="1")

    map_data = get_config("map_data")
    sections = map_data.sections()
    client = []
    if city_code == "1" or city_code == "2":
        if city_code == "1":
            client.append("SeoulBIS")

        for section in sections:
            western_min = map_data.getfloat(section, "western-outer-longitude", fallback=None)
            western_max = map_data.getfloat(section, "western-inner-longitude", fallback=None)
            eastern_min = map_data.getfloat(section, "eastern-inner-longitude", fallback=None)
            eastern_max = map_data.getfloat(section, "eastern-outer-longitude", fallback=None)
            inner = True
            if western_max is None and eastern_max is not None:
                western_max = eastern_max
                inner = False
            if eastern_min is None and western_min is not None:
                eastern_min = western_min
                inner = False

            southern_min = map_data.getfloat(section, "southern-outer-latitude", fallback=None)
            southern_max = map_data.getfloat(section, "southern-inner-latitude", fallback=None)
            northern_min = map_data.getfloat(section, "northern-inner-latitude", fallback=None)
            northern_max = map_data.getfloat(section, "northern-outer-latitude", fallback=None)
            if southern_max is None and northern_max is not None:
                southern_max = northern_max
                inner = False
            if northern_min is None and southern_min is not None:
                northern_min = southern_min
                inner = False
            _client = map_data.get(section, "client")

            if (
                western_min < pos_x < eastern_max and
                southern_min < pos_y < northern_max and
                _client not in client and (
                    inner and
                    not (
                        western_max < pos_x < eastern_min and
                        southern_max < pos_y < northern_min
                    ) or not inner
                )
            ):
                client.append(_client)

        result = []
        _list_ids = []
        for client_name in client:
            _client = getattr(bus_api, client_name)(token=token.seoul_bis)
            try:
                _result = _client.get_station_around(
                    pos_x=pos_x, pos_y=pos_y
                )
            except bus_api.EmptyData:
                continue

            for index, station in enumerate(_result):
                if station.id1 in _list_ids:
                    _index = _list_ids.index(station.id1)
                    if isinstance(result[_index].id2, list):
                        if station.id2 not in result[_index].id2:
                            result[_index].id2.append(station.id2)
                    else:
                        if int(result[_index].id2) == 0:
                            result[_index].id2 = station.id2
                            result[_index].type = station.type
                        elif result[_index].id2 != station.id2 and int(station.id2) != 0:
                            result[_index].id2 = [
                                result[_index].id2, station.id2
                            ]
                else:
                    _list_ids.append(station.id1)
                    result.append(station)
    elif city_code == "11":
        client = bus_api.SeoulBIS(token=token.seoul_bis)
        result = client.get_station_around(pos_x=pos_x, pos_y=pos_y)
    elif city_code == "12":
        client = bus_api.GyeonggiBIS(token=token.seoul_bis)
        result = client.get_station_around(pos_x=pos_x, pos_y=pos_y)
    elif city_code == "13":
        client = bus_api.IncheonBIS(token=token.seoul_bis)
        result = client.get_station_around(pos_x=pos_x, pos_y=pos_y)
    else:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Invalid City Code"
            }),
            400
        )
    final_result = [
        x.to_data() for x in result if x.id != 0
    ]
    final_result = sorted(final_result, key=lambda x: x['distance'])
    return jsonify(final_result)


@bp.route("/route", methods=['GET'])
def arrival_info():
    args = req.args
    if "id" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Bus Station ID."
            }),
            400
        )
    if "cityCode" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing City id."
            }),
            400
        )
    station_id = args['id']
    city_code = args.get('cityCode', type=int)

    client_namedtuple = namedtuple('client', ['seoul', 'gyeonggi', 'incheon', 'gyeonggi_arrival', 'incheon_arrival'])
    client = client_namedtuple(
        bus_api.SeoulBIS(token=token.seoul_bis),
        bus_api.GyeonggiBIS(token=token.gyeonggi_bis),
        bus_api.IncheonBIS(token=token.incheon_bis),
        bus_api.GyeonggiArrival(token=token.gyeonggi_arrival),
        bus_api.IncheonArrival(token=token.incheon_arrival)
    )

    result = []
    override = []
    if city_code == 11:
        try:
            _result = client.seoul.get_arrival(station_id=station_id)
        except bus_api.EmptyData:
            return jsonify([])
        _station_ids = _result[0].station.id1
        for bus in _result:
            if bus.bus_type != 8 and bus.bus_type != 7:
                result.append(
                    BusRouteInfo.from_seoul(bus)
                )
            elif bus.bus_type == 8 and client.gyeonggi_arrival not in override:
                override.append(client.gyeonggi_arrival)
            elif bus.bus_type == 7 and client.incheon_arrival not in override:
                override.append(client.incheon_arrival)

        if client.gyeonggi_arrival in override:
            result = get_gyeonggi(client, _station_ids, result)
        if client.incheon_arrival in override:
            result = get_incheon(client, _station_ids, result)
    elif city_code == 12 or city_code == 13:
        result = get_gyeonggi(client, station_id)
        result = get_incheon(client, station_id, result)
    return jsonify([
        x.to_dict() for x in result
    ])
