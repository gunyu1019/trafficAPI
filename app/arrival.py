from typing import List, Dict, Union

from app.modules import bus_api
from app.modules.bus_api.models.BusArrival import BusRouteInfo
from app.modules.bus_api.models.GyeonggiArrival import GyeonggiBusArrival
from app.modules.bus_api.models.IncheonArrival import IncheonBusArrival
from app.modules.bus_api.models.KoreaArrival import KoreaBusArrival
from app.modules.bus_api.models.ChangwonArrival import ChangwonBusArrival
from app.modules.bus_api.models.UlsanArrival import UlsanBusArrival


def get_gyeonggi(client, station_id: str, result: list = None, version: str = 'v1'):
    if result is None:
        result = []
    added_bus_id = []
    for bus in result:
        added_bus_id.append(bus.id)
    data = {}
    try:
        route_data = client.gyeonggi.get_route(station_id=station_id)
    except bus_api.EmptyData:
        return result

    arrival_data = []
    try:
        arrival_data = client.gyeonggi.get_arrival(station_id=station_id)
    except bus_api.EmptyData:
        pass

    for arrival in arrival_data:
        data[arrival.bus_id] = arrival

    for route in route_data:
        if route.id in added_bus_id:
            continue

        if route.id in data:
            result.append(
                BusRouteInfo.from_gyeonggi(route, data[route.id], version)
            )
        else:
            result.append(
                BusRouteInfo.from_gyeonggi(route, version)
            )
    return result


def get_incheon(client, station_id: str, result: list = None, version: str = 'v1'):
    if result is None:
        result = []
    added_bus_id = []
    for bus in result:
        added_bus_id.append(bus.id)

    data = {}
    try:
        route_data = client.incheon.get_route(station_id=station_id)
    except bus_api.EmptyData:
        return result

    arrival_data = []
    try:
        arrival_data = client.incheon.get_arrival(station_id=station_id)
    except bus_api.EmptyData:
        pass
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
        # if len(_arrival) < 2:
        #     [_arrival.append(IncheonBusArrival.empty()) for x in range(2 - len(_arrival))]
        result.append(
            BusRouteInfo.from_incheon(_route, _arrival, version)
        )
    return result


def get_changwon(client: bus_api.ChangwonBIS, arrival_data: ChangwonBusArrival):
    bus_data = client.get_bus_data()

    route = bus_data[bus_data['id'] == arrival_data.id].to_dict('records')[0]
    if route['color'] == 2:
        route_type = 1
    elif route['color'] == 5:
        route_type = 3
    elif route['color'] == 8:
        route_type = 4
    else:
        route_type = 2

    return BusRouteInfo.from_changwon(arrival_data, route, route_type)


def get_korea(arrival_data: List[KoreaBusArrival], route_data: List[bus_api.models.BusRoute], type_prefix: int):
    _route_data: Dict[int, Union[type(None), List[KoreaBusArrival], bus_api.models.BusRoute]] = {}
    for route in route_data:
        _route_data[route.id] = {
            "route": route,
            "arrival": []
        }

    for arrival in arrival_data:
        if arrival.bus_id not in _route_data:
            continue
        _route_data[arrival.bus_id]["arrival"].append(arrival)

    return [BusRouteInfo.from_korea(data["route"], data["arrival"], type_prefix) for data in _route_data.values()]


def get_ulsan(arrival_data: List[UlsanBusArrival], route_data: List[bus_api.models.BusRoute]):
    _route_data: Dict[int, Union[type(None), List[UlsanBusArrival], bus_api.models.BusRoute]] = {}
    for route in route_data:
        _route_data[int(route.id)] = {
            "route": route,
            "arrival": []
        }

    for arrival in arrival_data:
        if arrival.bus_id not in _route_data:
            continue
        _route_data[arrival.bus_id]["arrival"].append(arrival)

    return [BusRouteInfo.from_ulsan(data["route"], data["arrival"]) for data in _route_data.values()]
