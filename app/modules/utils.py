from collections import OrderedDict
from typing import Union, List, Any


def get_list_from_ordered_dict(
        data: Union[
            OrderedDict, List[OrderedDict]
        ]
) -> List[Any]:
    if isinstance(data, list):
        return data
    return [data]
