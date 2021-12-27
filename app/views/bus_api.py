from typing import NamedTuple, Optional

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
    korea_bis: str
    korea_arrival: str
    seoul_bis: str
    gyeonggi_bis: str
    gyeonggi_arrival: str


parser = get_config()
token = Token(
    korea_bis=parser.get("token", "KoreaBIS"),
    korea_arrival=parser.get("token", "KoreaArrival"),
    seoul_bis=parser.get("token", "SeoulBIS"),
    gyeonggi_bis=parser.get("token", "GyeonggiBIS"),
    gyeonggi_arrival=parser.get("token", "GyeonggiArrival")
)


class ArrivalData:
    def __init__(self, _token: Token):
        self.token = _token

    def seoul_data(self, data):
        bus_data = {}
        for d in data:
            bus_data[d.name] = {
                "busName": d.name,
                "busId": d.id,
                "busType": d.bus_type,
                "arrivalInfo": [
                    {
                        "vehicleType": d.vehicle_type1,
                        "prevStation": d.prev_count1,
                        "arrivalTime": d.time1,
                        "seat": None,
                        "carNumber": None,
                        "is_full": d.is_full1,
                        "is_arrival": d.is_arrive1
                    }, {
                        "vehicleType": d.vehicle_type2,
                        "prevStation": d.prev_count2,
                        "arrivalTime": d.time2,
                        "seat": None,
                        "carNumber": None,
                        "is_full": d.is_full2,
                        "is_arrival": d.is_arrive2
                    }
                ]
            }
        return bus_data

    def gyeonggi_data(self, bus_route, data):
        bus_data = {}
        routes = {}
        for r in bus_route:
            routes[r.id] = r
        for d in data:
            _bus_info = routes.get(d.bus_id)

            def convert_seat(people: int) -> Optional[int]:
                if people == -1:
                    return None
                return people

            bus_data[_bus_info.name] = {
                "busName": _bus_info.name,
                "busId": d.bus_id,
                "busType": _bus_info.type,

                "arrivalInfo": [
                    {
                        "vehicleType": d.vehicle_type1,
                        "prevStation": d.prev_count1,
                        "arrivalTime": d.time1,
                        "seat": convert_seat(d.seat1),
                        "carNumber": d.car_number1,
                        "is_full": True if d.seat1 == 0 else False,
                        "is_arrival": d.prev_count1 <= 1 if isinstance(d.prev_count1, int) else None
                    }, {
                        "vehicleType": d.vehicle_type2,
                        "prevStation": d.prev_count2,
                        "arrivalTime": d.time2,
                        "seat": convert_seat(d.seat2),
                        "carNumber": d.car_number2,
                        "is_full": True if d.seat2 == 0 else False,
                        "is_arrival": d.prev_count2 <= 1 if isinstance(d.prev_count2, int) else None
                    }
                ]
            }
        return bus_data

    def korea_data(self, data):
        bus_data = {}
        for d in data:
            if d.name not in bus_data:
                bus_data[d.name] = {
                    "busName": d.name,
                    "busId": d.id,
                    "busType": d.bus_type,
                    "arrivalInfo": []
                }
            elif len(bus_data[d.name]) >= 2:
                continue

            bus_data[d.name]["arrivalInfo"].append({
                "vehicleType": d.vehicle_type,
                "prevStation": d.prev_count,
                "arrivalTime": d.time,
                "seat": None,
                "carNumber": None,
                "is_full": None,
                "is_arrival": d.prev_count <= 1 if isinstance(d.prev_count, int) else None
            })
        return bus_data


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

    if city_id == "11":
        client = bus_api.SeoulBIS(token=token.seoul_bis)
        result = client.get_station(name=name)
        default_display_id = True
    elif city_id == "12" or city_id == "1":
        client = bus_api.GyeonggiBIS(token=token.seoul_bis)
        result = client.get_station(name=name)
        if city_id == "1":
            default_display_id = True
        else:
            default_display_id = False
    else:
        client = bus_api.KoreaBIS(token=token.korea_bis)
        result = client.get_station(city_code=city_id, name=name)
        default_display_id = False
    return jsonify([
        x.to_data(default_display_id) for x in result
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

    convert_client = ArrivalData(token)
    if city_id == "1":
        client = bus_api.SeoulBIS(token=token.seoul_bis)
        data = client.get_arrival(station_id=station_id)
        bus_data = convert_client.seoul_data(data=data)

        inject_data = {"GBUS": False}
        delete_key = []
        for bus in bus_data.values():
            if bus['busType'] == "8":
                inject_data["GBUS"] = True
                delete_key.append(bus['busName'])
            elif bus['busType'] == "7":
                # Incheon Bus Injection
                pass
        for key in delete_key:
            bus_data.pop(key)

        addition_data = {}
        addition_bus_data = {}
        if inject_data["GBUS"]:
            addition_client1 = bus_api.GyeonggiArrival(token=token.gyeonggi_arrival)
            addition_client2 = bus_api.GyeonggiBIS(token=token.gyeonggi_bis)
            _bus_route = addition_client2.get_route(station_id=data[0].station.id1)
            print(data[0].station.id1)
            addition_data["GBUS"] = addition_client1.get_arrival(station_id=data[0].station.id1)
            addition_bus_data["GBUS"] = convert_client.gyeonggi_data(data=addition_data["GBUS"], bus_route=_bus_route)

            for x in addition_bus_data["GBUS"].values():
                bus_data[x["busName"]] = x
    elif city_id == "11":
        client = bus_api.SeoulBIS(token=token.seoul_bis)
        data = client.get_arrival(station_id=station_id)
        bus_data = convert_client.seoul_data(data=data)
    elif city_id == "12":
        client1 = bus_api.GyeonggiArrival(token=token.gyeonggi_arrival)
        client2 = bus_api.GyeonggiBIS(token=token.gyeonggi_bis)
        bus_route = client2.get_route(station_id=station_id)
        data = client1.get_arrival(station_id=station_id)
        bus_data = convert_client.gyeonggi_data(data=data, bus_route=bus_route)
    else:
        client = bus_api.KoreaArrival(token=token.korea_arrival)
        data = client.get_arrival(city_code=city_id, station_id=station_id, rows=1000)
        bus_data = convert_client.korea_data(data=data)

    return jsonify(bus_data)


