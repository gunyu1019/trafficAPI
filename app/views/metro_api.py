import os
import re
import datetime
import pandas
import math
from typing import List

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.directory import directory
from app.modules.errors import EmptyData
from app.modules.metro import arrival, client, realtimeArrival, namedTupleModel
from app.utils import haversine

bp = Blueprint(
    name="metro_api",
    import_name="metro_api",
    url_prefix="/metro"
)
parser = get_config()
arrival_client = arrival.Arrival(parser.get("token", "SeoulRealtimeMetro"))
metro_client = client.Client(parser.get("token", "SeoulMetro"))

with open(os.path.join(directory, "data", "station_info.csv"), 'r', encoding='utf8') as fp:
    station_info = pandas.read_csv(fp)


with open(os.path.join(directory, "data", "station_position.csv"), 'r', encoding='utf8') as fp:
    station_position = pandas.read_csv(fp)


@bp.route("/arrival", methods=['GET'])
def arrival_info():
    args = req.args
    if "id" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Metro Station Id."
            }),
            400
        )
    pre_dict_data = station_info[station_info['stationId'] == int(args['id'])].to_dict('records')
    if len(pre_dict_data) < 1:
        return make_response(
            jsonify({
                "CODE": 404,
                "MESSAGE": "Unknown Station Id"
            }),
            404
        )
    elif len(pre_dict_data) > 1:
        return make_response(
            jsonify({
                "CODE": 500,
                "MESSAGE": "Failed to get station data"
            }),
            500
        )
    info = namedTupleModel.StationInfo(**pre_dict_data[0])
    try:
        arrival_data = arrival_client.arrival_info(name=info.name, start_index=1, end_index=1000)
    except EmptyData:
        arrival_data = []

    # 지하철역명의 부역명 제거
    pattern = re.compile(r"([가-핳|0-9a-zA-Z]+)(\([가-핳|0-9a-zA-Z]+\))")
    _real_name = pattern.search(info.name)
    if _real_name is None:
        real_name = info.name
    else:
        real_name = _real_name.groups()[0]

    # 갑 = 검색하는 역사 / 을 = 비교하는 역사
    # 1. 갑의 역명과 을의 본역명 비교
    # 2. 갑과 을의 값 비교 (동일)
    pre_transform = station_info[
        (station_info['name'].str.match(r"{}(\([가-핳|0-9a-zA-Z]+\))".format(real_name))) |
        (station_info['name'] == real_name)
        ].to_dict('records')
    transform = [namedTupleModel.StationInfo(**x) for x in pre_transform if x['stationId'] != info.stationId]

    def transform_arrival_loop(_arrival_data, _station: namedTupleModel.StationInfo) -> List[
        realtimeArrival.RealtimeArrival
    ]:
        if _station.name == info.name:
            return _arrival_data
        transform_arrival_data = arrival_client.arrival_info(name=_station.name, start_index=1, end_index=1000)
        return transform_arrival_data

    result = {
        "arrival": [x.to_dict() for x in arrival_data if x.subway == info.subway],
        "displayName": info.name,
        "subway": info.subway,
        "transform": {
            station.subway: {
                "arrival": [
                    transform_arrival.to_dict(add_subway=True)
                    for transform_arrival in transform_arrival_loop(arrival_data, station)
                    if int(transform_arrival.station) == station.stationId
                ],
                "displayName": station.name,
                "stationId": station.stationId
            } for station in transform
        },
        "stationName": real_name,
        "stationId": info.stationId
    }
    return jsonify(result)


@bp.route("/station", methods=['GET'])
def station_query():
    args = req.args
    if "name" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Metro Station name."
            }),
            400
        )
    name = args['name']
    try:
        station_data = metro_client.query(name=name, start_index=1, end_index=1000)
    except EmptyData:
        return make_response(
            jsonify({
                "CODE": 404,
                "MESSAGE": "Not Found."
            }),
            404
        )
    return jsonify([
        x.to_dict() for x in station_data
    ])


@bp.route("/timetable", methods=['GET'])
def timetable_info():
    args = req.args
    if "id" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Metro Station Id."
            }),
            400
        )
    weekday = datetime.datetime.now().weekday()
    default_week_type = 0
    if 0 <= weekday <= 4:
        default_week_type = 0
    elif 4 < weekday <= 5:
        default_week_type = 1
    elif 5 < weekday <= 6:
        default_week_type = 2

    station_id = args['id']
    direction = args.get("direction", type=int, default=0) + 1
    week_type = args.get("weekType", type=int, default=default_week_type) + 1
    if not(0 < direction < 3):
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Wrong direction."
            }),
            400
        )
    if not(0 < week_type < 4):
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Wrong weekType."
            }),
            400
        )
    try:
        timetable_data = metro_client.timetable(
            station_id=station_id,
            start_index=1,
            end_index=1000,
            direction=direction,
            time_type=week_type
        )
    except EmptyData:
        timetable_data = []
    return jsonify([
        x.to_dict() for x in sorted(timetable_data, key=lambda x:(x.hours, x.minutes, x.seconds))
    ])


@bp.route("/around", methods=['GET'])
def around_info():
    args = req.args
    if "posX" not in args or "posY" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing posX or posY."
            }),
            400
        )
    distance = args.get('distance', type=int, default=500)
    details = args.get('details', type=bool, default=True)
    pos_x = args.get('posX', type=float)
    pos_y = args.get('posY', type=float)
    stations = [
        namedTupleModel.StationPosition(**station).name
        for station in station_position.to_dict('records')
        if haversine(station['posX'], station['posY'], pos_x, pos_y) <= distance
    ]
    if not details:
        return jsonify(stations)
    result = {}
    for name in stations:
        try:
            data = metro_client.query(name=name, start_index=1, end_index=1000)
            relative_pos_x = data[0].pos_x - pos_x
            relative_pos_y = data[0].pos_y - pos_y
            result[name] = {
                "distance": round(
                    haversine(data[0].pos_x, data[0].pos_y, pos_x, pos_y), 2
                ),
                "data": [x.to_dict_for_around() for x in data],
                "direction": int(
                    round(math.atan2(relative_pos_x, relative_pos_y) * 180 / math.pi)
                ),
                "posX": data[0].pos_x,
                "posY": data[0].pos_y
            }
        except EmptyData:
            continue
    return jsonify(result)
