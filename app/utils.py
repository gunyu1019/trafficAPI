import math
from collections import OrderedDict
from typing import Union, List, Any, Optional


def get_list_from_ordered_dict(
        data: Union[
            OrderedDict, List[OrderedDict]
        ]
) -> List[Any]:
    if isinstance(data, list):
        return data
    return [data]


def get_int(data) -> Optional[int]:
    if isinstance(data, str) or isinstance(data, int):
        return int(data)
    return None


def get_float(data) -> Optional[float]:
    if isinstance(data, str) or isinstance(data, float):
        return float(data)
    return None


# mean earth radius - https://en.wikipedia.org/wiki/Earth_radius#Mean_radius
EARTH_RADIUS_M = 6371.0088 * 1000.0


def haversine(pos_x1, pos_y1, pos_x2, pos_y2):
    _pos_x1 = math.radians(pos_x1)
    _pos_x2 = math.radians(pos_x2)
    _pos_y1 = math.radians(pos_y1)
    _pos_y2 = math.radians(pos_y2)

    relative_x = _pos_x1 - _pos_x2
    relative_y = _pos_y1 - _pos_y2

    distance = math.sin(relative_y * 0.5) ** 2 + math.cos(_pos_y1) * math.cos(_pos_y2) * math.sin(relative_x * 0.5) ** 2
    return math.asin(math.sqrt(distance)) * EARTH_RADIUS_M * 2


def optional_int_to_str(data):
    if isinstance(data, int):
        return str(data)
    return data
