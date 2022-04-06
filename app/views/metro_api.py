import os
import re
import json
import pandas
from datetime import datetime
from typing import NamedTuple, List, Tuple, Optional

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.directory import directory
from app.modules.metro import arrival
from app.modules.errors import EmptyData

bp = Blueprint(
    name="metro_api",
    import_name="metro_api",
    url_prefix="/metro"
)
parser = get_config()
arrival_client = arrival.Arrival(parser.get("token", "SeoulMetro"))

with open(os.path.join(directory, "data", "station_info.csv"), 'r', encoding='cp949') as fp:
    station_info = pandas.read_csv(fp)


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
                "MESSAGE": "Missing Metro Station name."
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
    result = {
        "arrival": [x.to_dict() for x in arrival_data if x.subway == info.subway],
        "subway": info.subway,
        "transform": {
            station.subway: {
                "arrival": [
                    transform_arrival.to_dict(add_subway=True)
                    for transform_arrival in arrival_data if int(transform_arrival.station) == station.stationId
                ],
                "stationName(Real)": station.name,
                "stationId": station.stationId
            } for station in transform
        },
        "stationName": real_name,
        "stationId": info.stationId,
        "stationName(real)": info.name
    }
    return jsonify(result)
