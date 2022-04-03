import os
import json
from datetime import datetime
from typing import NamedTuple, List

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.directory import directory
from app.modules.bike_api.client import Client
from app.modules.bike_api.rideBike import RideBike

bp = Blueprint(
    name="bicycle_api",
    import_name="bicycle_api",
    url_prefix="/bike"
)
parser = get_config()
token = parser.get("token", "SeoulBike")
client = Client(token)


class BikeData(NamedTuple):
    data: List[RideBike]
    datetime: datetime


def load_bike_data() -> BikeData:
    with open(os.path.join(directory, "data", "bike_data.json"), "r", encoding='utf8') as fp:
        pre_data = json.load(fp)
    data = [RideBike.from_dict(x) for x in pre_data['data']]
    last_update = datetime.fromtimestamp(pre_data['lastUpdate'])
    if (datetime.now() - last_update).total_seconds() >= 1800:
        index = 0
        post_data = []
        while True:
            _data = client.bike_list(index * 1000 + 1, index * 1000 + 1000)
            post_data += _data
            if len(_data) < 900:
                break
            index += 1

        last_update = datetime.now().timestamp()
        with open(os.path.join(directory, "data", "bike_data.json"), "w", encoding='utf8') as fp:
            json.dump(
                {
                    "data": [x.to_dict() for x in post_data],
                    "lastUpdate": last_update
                }, fp, ensure_ascii=False, indent=4
            )
        data = post_data
    return BikeData(data, last_update)


@bp.route('/query', methods=['GET'])
def query_bike_info():
    args = req.args
    if "name" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Bike Station name."
            }),
            400
        )
    bike_name = args.get('name')
    data = load_bike_data()
    return jsonify({
        "data": [station.to_dict() for station in data.data if bike_name in station.name],
        "lastUpdate": data.datetime.timestamp()
    })


@bp.route('/around', methods=['GET'])
def around_bike_info():
    args = req.args
    if "posX" not in args or "posY" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing posX or posY."
            }),
            400
        )
    distance = args.get('distance', type=int)
    pos_x = args.get('posX', type=float)
    pos_y = args.get('posY', type=float)
    return
