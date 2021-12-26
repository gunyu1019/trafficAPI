from flask import Blueprint
from flask import jsonify
from flask import make_response
from flask import request as req
from typing import NamedTuple
from urllib import parse

from app.config.config import get_config
from app.modules import bus_api


bp = Blueprint(
    name="bus_api",
    import_name="bus_api",
    url_prefix="/bus"
)


class Token(NamedTuple):
    korea_bis: str
    korea_arrival: str
    seoul_bis: str


parser = get_config()
token = Token(
    korea_bis=parser.get("token", "KoreaBIS"),
    korea_arrival=parser.get("token", "KoreaArrival"),
    seoul_bis=parser.get("token", "SeoulBIS")
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

    if "cityId" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing City id."
            }),
            400
        )
    name = args['name']
    city_id = args['cityId']

    if city_id == "1":
        client = bus_api.SeoulBIS(token=token.seoul_bis)
        result = client.get_station(name=name)
    else:
        client = bus_api.KoreaBIS(token=token.korea_bis)
        result = client.get_station(city_code=city_id, name=name)
    return jsonify([
        x.to_data() for x in result
    ])


@bp.route("/arrival", methods=['GET'])
def station_arrival():
    args = req.args

    if "id" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing Bus Station name."
            }),
            400
        )

    if "cityId" not in args:
        return make_response(
            jsonify({
                "CODE": 400,
                "MESSAGE": "Missing City id."
            }),
            400
        )
    station_id = args['id']
    city_id = args['cityId']

    bus_data = {}
    if city_id == "1":
        client = bus_api.SeoulBIS(token=token.seoul_bis)
        data = client.get_arrival(station_id=station_id)
        for d in data:
            bus_data[d.name] = [{
                "busName": d.name,
                "busId": d.id,
                "busType": d.bus_type,
                "vehicleType": d.vehicle_type1,
                "prevStation": d.prev_count1,
                "arrivalTime": d.time1
            }, {
                "busName": d.name,
                "busId": d.id,
                "busType": d.bus_type,
                "vehicleType": d.vehicle_type2,
                "prevStation": d.prev_count2,
                "arrivalTime": d.time2
            }]
    else:
        client = bus_api.KoreaArrival(token=token.korea_arrival)
        data = client.get_arrival(city_code=city_id, station_id=station_id, rows=1000)
        for d in data:
            if d.name not in bus_data:
                bus_data[d.name] = []
            elif len(bus_data[d.name]) >= 2:
                continue

            bus_data[d.name].append({
                "busName": d.name,
                "busId": d.id,
                "busType": d.bus_type,
                "vehicleType": True if d.vehicle_type == "저상버스" else False,
                "prevStation": d.prev_count,
                "arrivalTime": d.time
            })

    return jsonify(bus_data)
