from typing import NamedTuple

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.modules import bus_api

bp = Blueprint(
    name="bus_api",
    import_name="bus_api",
    url_prefix="/bus"
)


class Token(NamedTuple):
    seoul_bus: str
    seoul_route: str
    gyeonggi_bus: str
    gyeonggi_route: str
    incheon_bus: str
    incheon_route: str


class ClientList(NamedTuple):
    seoul: bus_api.SeoulBIS
    gyeonggi: bus_api.GyeonggiBIS
    incheon: bus_api.IncheonBIS


parser = get_config()
token = Token(
    seoul_bus=parser.get("token", "SeoulBIS"),
    seoul_route=parser.get("token", "SeoulBIS"),
    gyeonggi_bus=parser.get("token", "GyeonggiBIS"),
    gyeonggi_route=parser.get("token", "GyeonggiArrival"),
    incheon_bus=parser.get("token", "IncheonBIS"),
    incheon_route=parser.get("token", "IncheonArrival")
)
client = ClientList(
    bus_api.SeoulBIS(token=token.seoul_bis),
    bus_api.GyeonggiBIS(token=token.gyeonggi_bis, arrival_token=token.gyeonggi_arrival),
    bus_api.IncheonBIS(token=token.incheon_bis, arrival_token=token.incheon_arrival)
)


@bp.route("/bus", methods=['GET'])
def bus_info():
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
    if city_code == "1":
        for client in []
    return
