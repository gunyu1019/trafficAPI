from typing import List, Tuple, Dict, Union
from .modules.stop_api import BusStation
from .utils import haversine


def conversion_metropolitan(
        pre_data: List[BusStation],
        exists_id: List[int] = None,
        default_result=None
) -> Tuple[
    List[BusStation],
    List[int]
]:
    result = default_result
    if exists_id is None:
        exists_id = []
    if result is None:
        result = []
    for index, station in enumerate(pre_data):
        if station.id1 in exists_id:
            _index = exists_id.index(station.id1)
            if isinstance(result[_index].id2, list):
                if station.id2 not in result[_index].id2:
                    result[_index].id2.append(station.id2)
            else:
                if int(result[_index].id2) == 0:
                    result[_index].id2 = station.id2
                    result[_index].type = station.type
                elif result[_index].id2 != station.id2 and int(station.id2) != 0:
                    result[_index].id2 = [
                        result[_index].id2, station.id2
                    ]
        else:
            exists_id.append(station.id1)
            result.append(station)
    return (
        result, exists_id
    )


def conversion_others(
        station_list: Dict[
            str, Dict[
                Union[int, str], List[BusStation]
            ]
        ],
        city_key: List[
            Union[str, int]
        ]
) -> List[BusStation]:
    result = []
    for station in station_list.values():
        if len(station.keys()) <= 1:
            for _city_code in station.values():
                for _station in _city_code:
                    _station.type = 200 + 2 ** (city_key.index(_station.type))
                    result.append(_station)
            continue
        keys = list(station.keys())

        v_station = {}
        for basic_station in station[keys[0]]:
            v_station[basic_station.id] = {
                "station": [],
                "info": basic_station
            }

        for _city_code in keys[1:]:
            _list_id = []
            for basic_station in station[keys[0]]:
                min_distance = 500
                candidate = None
                for other_station in station[_city_code]:
                    if other_station.id in _list_id:
                        continue
                    distance = haversine(
                        basic_station.pos_x, basic_station.pos_y, other_station.pos_x, other_station.pos_y
                    )
                    if distance <= min_distance:
                        min_distance = distance
                        candidate = other_station
                if candidate is None:
                    continue
                _list_id.append(candidate.id)
                v_station[basic_station.id]["station"].append(candidate)

        for basic_station in v_station.keys():
            info: BusStation = v_station[basic_station]['info']
            info.type = 200 + 2 ** (city_key.index(info.type))
            for other_station in v_station[basic_station]["station"]:
                if info.id2 is not None:
                    if not isinstance(info.id2, list):
                        info.id2 = [info.id2]

                    if other_station.id2 is not None:
                        info.id2.append(other_station.id2)
                else:
                    info.id2 = other_station.id2

                info.id1 = -2
                info.id1s.append(other_station.id1)
                info.type += 2 ** (city_key.index(other_station.type))
            result.append(info)
    return result
