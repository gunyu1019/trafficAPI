from typing import NamedTuple

from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req

from app.config.config import get_config
from app.conversion import conversion_metropolitan
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
    bus_api.SeoulBIS(bus_token=token.seoul_bus, location_token=token.seoul_route),
    bus_api.GyeonggiBIS(bus_token=token.gyeonggi_bus, location_token=token.gyeonggi_route),
    bus_api.IncheonBIS(bus_token=token.incheon_bus, location_token=token.incheon_route)
)


@bp.route("/search", methods=['GET'])
async def bus_info():
    args = req.args
    if "name" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Bus route name."
            }),
            400
        )
    bus_name = args.get('name')
    city_code = args.get('cityCode', default="1")
    result = []
    if city_code == "1":
        _list_ids = []
        try:
            _result = await client.seoul.get_bus(name=bus_name)
            result = [bus for bus in _result if bus.type != "1107" and bus.type != "1108"]
        except bus_api.EmptyData:
            pass

        for _client in [client.gyeonggi, client.incheon]:
            try:
                result += await _client.get_bus(name=bus_name)
            except bus_api.EmptyData:
                pass
    else:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Invalid City Code"
            }),
            400
        )
    return jsonify([
        x.to_dict() for x in result
    ])


@bp.route("/detail", methods=['GET'])
async def bus_info_detail():
    args = req.args
    if "id" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Bus ID."
            }),
            400
        )
    bus_id = args.get('id')
    city_code = args.get('cityCode', default="1")
    try:
        if city_code == "11":
            result = await client.seoul.get_bus_detail(bus_id=bus_id)
        elif city_code == "12":
            result = await client.gyeonggi.get_bus_detail(bus_id=bus_id)
        elif city_code == "13":
            result = await client.incheon.get_bus_detail(bus_id=bus_id)
        else:
            return make_response(
                jsonify({
                    "CODE": 400,
                    "MESSAGE": "Invalid City Code"
                }),
                400
            )
    except bus_api.EmptyData:
        return jsonify({})
    return jsonify(result.to_dict())


@bp.route("/busRoute", methods=['GET'])
async def bus_route():
    args = req.args
    if "id" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Bus ID."
            }),
            400
        )
    bus_id = args.get('id')
    city_code = args.get('cityCode', default="1")
    try:
        if city_code == "11":
            result = await client.seoul.get_bus_route(bus_id=bus_id)
        elif city_code == "12":
            result = await client.gyeonggi.get_bus_route(bus_id=bus_id)
        elif city_code == "13":
            result = await client.incheon.get_bus_route(bus_id=bus_id)
        else:
            return make_response(
                jsonify({
                    "CODE": 400,
                    "MESSAGE": "Invalid City Code"
                }),
                400
            )
    except bus_api.EmptyData:
        return jsonify([])
    return jsonify([
        x.to_dict() for x in result
    ])


@bp.route("/location", methods=['GET'])
async def bus_location():
    args = req.args
    if "id" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Bus ID."
            }),
            400
        )
    bus_id = args.get('id')
    city_code = args.get('cityCode', default="1")
    try:
        if city_code == "11":
            result = await client.seoul.get_bus_location(bus_id=bus_id)
        elif city_code == "12":
            result = await client.gyeonggi.get_bus_location(bus_id=bus_id)
        elif city_code == "13":
            result = await client.incheon.get_bus_location(bus_id=bus_id)
        else:
            return make_response(
                jsonify({
                    "CODE": 400,
                    "MESSAGE": "Invalid City Code"
                }),
                400
            )
    except bus_api.EmptyData:
        return jsonify([])
    return jsonify([
        x.to_dict() for x in result
    ])
