import os
import re
from typing import NamedTuple, List, Optional

import pandas
from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.directory import directory
from app.modules.errors import EmptyData
from app.modules.metro import arrival, client, realtimeArrival

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


with open(os.path.join(directory, "data", "subway.csv"), 'r', encoding='utf8') as fp:
    subway_info = pandas.read_csv(fp)


class SubwayInfo(NamedTuple):
    subwayId: Optional[int]
    name: str
    inSubwayId: Optional[str]


class StationInfo(NamedTuple):
    subway: int
    stationId: int
    name: str


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
    info = StationInfo(**pre_dict_data[0])
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
    transform = [StationInfo(**x) for x in pre_transform if x['stationId'] != info.stationId]

    def transform_arrival_loop(_arrival_data, _station: StationInfo) -> List[realtimeArrival.RealtimeArrival]:
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
    station_data = metro_client.query(name=name, start_index=1, end_index=1000)
    for index, _station_data in enumerate(station_data):
        _subway_info = subway_info[subway_info['inSubwayId'] == _station_data.line_number].to_dict('records')
        subway = None
        if len(_subway_info) > 0:
            subway = SubwayInfo(
                **_subway_info[0]
            )
            setattr(station_data[index], "_subway", subway)

        _arrival_station_info = station_info[(station_info['subway'] == subway.subwayId) & (station_info['name'].str.contains(name))].to_dict('records')
        if len(_arrival_station_info) > 0:
            arrival_station_info = StationInfo(
                **_arrival_station_info[0]
            )
            setattr(station_data[index], "_arrival_station", arrival_station_info.stationId)
    return jsonify([
        x.to_dict() for x in station_data
    ])
