from typing import NamedTuple

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.arrival import get_incheon, get_gyeonggi, get_changwon, get_korea, get_ulsan
from app.config.config import get_config
from app.conversion import conversion_metropolitan, conversion_others
from app.modules import stop_api
from app.modules.stop_api.models.BusArrival import BusRouteInfo

bp = Blueprint(
    name="stop_api",
    import_name="stop_api",
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
    changwon_bis: str
    changwon_arrival: str
    ulsan_bis: str


class ClientList(NamedTuple):
    seoul: stop_api.SeoulBIS
    gyeonggi: stop_api.GyeonggiBIS
    incheon: stop_api.IncheonBIS
    busan: stop_api.BusanBIS
    ulsan: stop_api.UlsanBIS
    changwon: stop_api.ChangwonBIS
    gimhae: stop_api.KoreaBIS


parser = get_config()
token = Token(
    korea_bis=parser.get("token", "KoreaBIS"),
    korea_arrival=parser.get("token", "KoreaArrival"),
    seoul_bis=parser.get("token", "SeoulBIS"),
    gyeonggi_bis=parser.get("token", "GyeonggiBIS"),
    gyeonggi_arrival=parser.get("token", "GyeonggiArrival"),
    incheon_bis=parser.get("token", "IncheonBIS"),
    incheon_arrival=parser.get("token", "IncheonArrival"),
    busan_bis=parser.get("token", "BusanBIS"),
    changwon_bis=parser.get("token", "ChangwonBIS"),
    changwon_arrival=parser.get("token", "ChangwonArrival"),
    ulsan_bis=parser.get("token", "UlsanBIS"),
)
client = ClientList(
    stop_api.SeoulBIS(token=token.seoul_bis),
    stop_api.GyeonggiBIS(token=token.gyeonggi_bis, arrival_token=token.gyeonggi_arrival),
    stop_api.IncheonBIS(token=token.incheon_bis, arrival_token=token.incheon_arrival),
    stop_api.BusanBIS(token=token.busan_bis),
    stop_api.UlsanBIS(token=token.ulsan_bis, korea_token=token.korea_bis),
    stop_api.ChangwonBIS(token=token.changwon_bis, arrival_token=token.changwon_arrival),
    stop_api.KoreaBIS(token=token.korea_bis, city_code=38070)
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
        try:
            result = client.seoul.get_station(name=station_name)
        except stop_api.EmptyData:
            result = []
    elif city_code == "12":
        try:
            result = client.gyeonggi.get_station(name=station_name)
        except stop_api.EmptyData:
            result = []
    elif city_code == "13":
        try:
            result = client.incheon.get_station(name=station_name)
        except stop_api.EmptyData:
            result = []
    elif city_code == "21":
        try:
            result = client.busan.get_station(name=station_name)
        except stop_api.EmptyData:
            result = []
    elif city_code == "22":
        try:
            result = client.ulsan.get_station(name=station_name)
        except stop_api.EmptyData:
            result = []
    elif city_code == "24":
        try:
            result = client.changwon.get_station(name=station_name)
        except stop_api.EmptyData:
            result = []
    elif city_code == "25":
        try:
            result = client.gimhae.get_station(name=station_name)
        except stop_api.EmptyData:
            result = []
    elif city_code == "1":
        matched_client = [client.seoul, client.gyeonggi, client.incheon]
        result = []
        _list_ids = []

        for _client in matched_client:
            try:
                client_result = _client.get_station(name=station_name)
            except stop_api.EmptyData:
                continue

            result, _list_ids = conversion_metropolitan(
                client_result, _list_ids, result
            )
    elif city_code == "3":
        city_key = ["BUSAN", "ULSAN", "CHANGWON", 38070]
        matched_client = [
            stop_api.BusanBIS(token=token.busan_bis),
            stop_api.UlsanBIS(token=token.ulsan_bis, korea_token=token.korea_bis),
            stop_api.ChangwonBIS(token=token.changwon_bis, arrival_token=token.changwon_arrival),
            stop_api.KoreaBIS(token=token.korea_bis, city_code=city_key[3])
        ]  # 1 2 4 8
        station_list = {}

        for _client in matched_client:
            try:
                _result = _client.get_station(name=station_name)
            except stop_api.EmptyData:
                continue

            for station in _result:
                if station.name.startswith("사용안함") or station.name.endswith('미사용'):
                    continue

                if station.name not in station_list:
                    station_list[station.name] = {}
                if station.type not in station_list[station.name]:
                    station_list[station.name][station.type] = []
                station_list[station.name][station.type].append(station)

        result = conversion_others(station_list, city_key)
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
    matched_client = []
    metropolitan = False
    if city_code == "1" or city_code == "2":
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
                matched_client.append(_client)

            if 'gyeonggi' in matched_client or 'incheon' in matched_client or 'seoul' in matched_client:
                metropolitan = True
                if city_code == "1" and 'seoul' not in matched_client:
                    matched_client.append("seoul")

        pre_result = {}
        result = []
        _list_ids = []
        for client_name in matched_client:
            _client = getattr(client, client_name)
            try:
                client_result = _client.get_station_around(
                    pos_x=pos_x, pos_y=pos_y
                )
            except stop_api.EmptyData:
                continue

            if metropolitan:
                result, _list_ids = conversion_metropolitan(
                    client_result, _list_ids, result
                )
            else:
                for station in client_result:
                    if station.name.startswith("사용안함") or station.name.endswith('미사용'):
                        continue

                    if station.name not in pre_result:
                        pre_result[station.name] = {}
                    if station.type not in pre_result[station.name]:
                        pre_result[station.name][station.type] = []
                    pre_result[station.name][station.type].append(station)

        if not metropolitan:
            result = conversion_others(pre_result, ["BUSAN", "ULSAN", "CHANGWON", 38070])
    elif city_code == "11":
        result = client.seoul.get_station_around(pos_x=pos_x, pos_y=pos_y)
    elif city_code == "12":
        result = client.gyeonggi.get_station_around(pos_x=pos_x, pos_y=pos_y)
    elif city_code == "13":
        result = client.incheon.get_station_around(pos_x=pos_x, pos_y=pos_y)
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
    version = args.get('version', type=str, default='v1')

    result = []
    override = []
    if city_code == 11:
        try:
            _result = client.seoul.get_arrival(station_id=station_id)
        except stop_api.EmptyData:
            return jsonify([])
        _station_ids = _result[0].station.id1
        for bus in _result:
            if bus.bus_type != 8 and bus.bus_type != 7:
                result.append(
                    BusRouteInfo.from_seoul(bus, version)
                )
            elif bus.bus_type == 8 and client.gyeonggi not in override:
                override.append(client.gyeonggi)
            elif bus.bus_type == 7 and client.incheon not in override:
                override.append(client.incheon)

        if client.gyeonggi in override:
            result = get_gyeonggi(client, _station_ids, result, version=version)
        if client.incheon in override:
            result = get_incheon(client, _station_ids, result, version=version)
    elif city_code == 12 or city_code == 13:
        result = get_gyeonggi(client, station_id, version=version)
        result = get_incheon(client, station_id, result, version)
    elif 200 < city_code < 264:
        city_key = ['busan', 'ulsan', 'changwon', 'gimhae']
        bus_type_dictionary = {
            "gimhae": {"지선버스": 1, "급행버스": 2}
        }
        prefix_route = [21, 22, 24, 25]
        station_ids = list(reversed(station_id.split(',')))
        client_by_station_id = []
        test_city_code = int(city_code) - 200
        t = 0
        for _, client_name in enumerate(reversed(city_key)):
            index = city_key.index(client_name)
            if test_city_code - 2 ** index >= 0:
                test_city_code -= 2 ** index
                _client = getattr(client, client_name)
                client_by_station_id.append((_client, station_ids[t], city_key[index]))
                if test_city_code == 0:
                    break
                t += 1
        client_by_station_id.reverse()
        for _client, _station_id, city_id in client_by_station_id:
            try:
                _result = _client.get_arrival(_station_id)
            except stop_api.EmptyData:
                _result = []

            if city_id not in ["busan", "changwon", "ulsan"]:
                index = city_key.index(city_id)
                try:
                    route_data = _client.get_route(_station_id, bus_type_dictionary[city_id])
                except stop_api.EmptyData:
                    continue
                result += get_korea(_result, route_data, prefix_route[index])
                continue
            elif city_id == "ulsan":
                route_data = _client.get_route(_station_id)
                result += get_ulsan(_result, route_data)
                continue

            for route in _result:
                if city_id == "busan":
                    result.append(BusRouteInfo.from_busan(route))
                elif city_id == "changwon":
                    result.append(get_changwon(_client, route))
    return jsonify([
        x.to_dict() for x in result
    ])
