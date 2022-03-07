from typing import NamedTuple
from collections import namedtuple

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.modules import bus_api
from app.modules.bus_api.models.BusArrival import BusRouteInfo
from app.modules.bus_api.models.GyeonggiArrival import GyeonggiBusArrival
from app.modules.bus_api.models.IncheonArrival import IncheonBusArrival

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


parser = get_config()
token = Token(
    korea_bis=parser.get("token", "KoreaBIS"),
    korea_arrival=parser.get("token", "KoreaArrival"),
    seoul_bis=parser.get("token", "SeoulBIS"),
    gyeonggi_bis=parser.get("token", "GyeonggiBIS"),
    gyeonggi_arrival=parser.get("token", "GyeonggiArrival"),
    incheon_bis=parser.get("token", "IncheonBIS"),
    incheon_arrival=parser.get("token", "IncheonArrival")
)


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
        client = bus_api.SeoulBIS(token=token.seoul_bis)
        result = client.get_station(name=station_name)
    elif city_code == "12":
        client = bus_api.GyeonggiBIS(token=token.seoul_bis)
        result = client.get_station(name=station_name)
    elif city_code == "13":
        client = bus_api.IncheonBIS(token=token.seoul_bis)
        result = client.get_station(name=station_name)
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
                # print(station.name, station.id1, station.id2, station.type)
                if station.id1 in _list_ids:
                    _index = _list_ids.index(station.id1)
                    if isinstance(result[_index].id2, list):
                        if station.id2 not in result[_index].id2:
                            result[_index].id2.append(station.id2)
                    else:
                        if result[_index].id2 == 0:
                            result[_index].id2 = station.id2
                            result[_index].type = station.type
                        elif result[_index].id2 != station.id2 and station.id2 != 0:
                            result[_index].id2 = [
                                result[_index].id2, station.id2
                            ]
                else:
                    _list_ids.append(station.id1)
                    result.append(station)
    else:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Invalid City Code"
            }),
            400
        )
    return jsonify([
        x.to_data() for x in result
    ])


def get_gyeonggi(client, station_id: str, result: list = None):
    if result is None:
        result = []
    data = {}
    try:
        arrival_data = client.gyeonggi_arrival.get_arrival(station_id=station_id)
        route_data = client.gyeonggi.get_route(station_id=station_id)
    except bus_api.EmptyData:
        return result
    for arrival in arrival_data:
        data[arrival.bus_id] = arrival

    for route in route_data:
        if route.district == 1 or route.district == 3:
            continue

        if route.id in data:
            result.append(
                BusRouteInfo.from_gyeonggi(route, data[route.id])
            )
        else:
            result.append(
                BusRouteInfo.from_gyeonggi(route, GyeonggiBusArrival.empty())
            )
    return result


def get_incheon(client, station_id: str, result: list = None):
    if result is None:
        result = []
    added_bus_id = []
    for bus in result:
        added_bus_id.append(bus.id)

    data = {}
    try:
        arrival_data = client.incheon_arrival.get_arrival(station_id=station_id)
        route_data = client.incheon.get_route(station_id=station_id)
    except bus_api.EmptyData:
        return result
    for route in route_data:
        if route.id not in added_bus_id:
            data[route.id] = {
                "data": route,
                "arrival": []
            }

    for arrival in arrival_data:
        if arrival.id in data:
            data[arrival.id]['arrival'].append(arrival)

    for route_id in data.keys():
        _route = data[route_id]['data']
        _arrival = data[route_id]['arrival']
        if len(_arrival) < 2:
            [_arrival.append(IncheonBusArrival.empty()) for x in range(2 - len(_arrival))]
        result.append(
            BusRouteInfo.from_incheon(_route, _arrival)
        )
    return result


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
