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
