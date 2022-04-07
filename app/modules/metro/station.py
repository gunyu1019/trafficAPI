import os
import pandas

from typing import Any, Dict
from app.directory import directory
from app.modules.metro import namedTupleModel

with open(os.path.join(directory, "data", "station_info.csv"), 'r', encoding='utf8') as fp:
    station_info = pandas.read_csv(fp)


with open(os.path.join(directory, "data", "subway.csv"), 'r', encoding='utf8') as fp:
    subway_info = pandas.read_csv(fp)


class Station:
    def __init__(self, **kwargs):
        self.id = kwargs['station_id']
        self.code = kwargs['code']
        self.name = kwargs['name']
        self.arrival_id = kwargs.get('arrival_id')
        self.display_name = kwargs.get('display_name')
        self.subway = kwargs.get('subway')
        self.subway_id = kwargs.get('subway_id')

        self._line_id = kwargs['line_id']

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        line_number = payload.get("LINE_NUM")
        name = payload.get("STATION_NM")
        _subway_info = subway_info[subway_info['inSubwayId'] == line_number].to_dict('records')
        subway = namedTupleModel.SubwayInfo()
        if len(_subway_info) > 0:
            subway = namedTupleModel.SubwayInfo(
                **_subway_info[0]
            )
        elif len(_subway_info) > 1:
            raise Exception("Incorrect Subway Info")

        arrival_station = namedTupleModel.StationInfo()
        if subway is not None:
            _arrival_station = station_info[
                (station_info['subway'] == subway.subwayId) & (
                    (station_info['name'] == name) |
                    (station_info['name'].str.match(r"{}(\([가-핳|0-9a-zA-Z]+\))".format(name)))
                )
            ].to_dict('records')
            if len(_arrival_station) > 0:
                arrival_station = namedTupleModel.StationInfo(
                    **_arrival_station[0]
                )
            elif len(_arrival_station) > 1:
                raise Exception("Incorrect Subway Info")
        return cls(
            arrival_id=arrival_station.stationId,
            display_name=arrival_station.name,
            code=payload.get("FR_CODE"),
            name=name,
            station_id=payload.get("STATION_CD"),
            line_id=line_number,
            subway=subway.name,
            subway_id=subway.subwayId if subway.subwayId != 0 else None
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "arrivalStationId": self.arrival_id,
            "displayName": self.display_name,
            "code": self.code,
            "name": self.name,
            "id": self.id,
            "subway": self.subway,
            "subwayId": self.subway_id
        }
