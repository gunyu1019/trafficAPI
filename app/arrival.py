from app.modules import bus_api
from app.modules.bus_api.models.BusArrival import BusRouteInfo
from app.modules.bus_api.models.GyeonggiArrival import GyeonggiBusArrival
from app.modules.bus_api.models.IncheonArrival import IncheonBusArrival


def get_gyeonggi(client, station_id: str, result: list = None):
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
        arrival_data = client.gyeonggi_arrival.get_arrival(station_id=station_id)
    except bus_api.EmptyData:
        pass

    for arrival in arrival_data:
        data[arrival.bus_id] = arrival

    for route in route_data:
        if route.id in added_bus_id:
            continue

        if route.id in data:
            result.append(
                BusRouteInfo.from_gyeonggi(route, data[route.id])
            )
        else:
            result.append(
                BusRouteInfo.from_gyeonggi(route)
            )
    return result


def get_incheon(client, station_id: str, result: list = None):
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
        arrival_data = client.incheon_arrival.get_arrival(station_id=station_id)
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
            BusRouteInfo.from_incheon(_route, _arrival)
        )
    return result


def get_korea(client, station_id: str, result: list = None):
    if result is None:
        result = []

    try:
        route_data = client.get_route(station_id=station_id)
    except bus_api.EmptyData:
        return result
    return