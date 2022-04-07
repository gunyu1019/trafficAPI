from app.modules.baseClient import BaseClient
from app.modules.errors import EmptyData
from .station import Station


class Client(BaseClient):
    def __init__(self, token: str):
        super().__init__("http://openapi.seoul.go.kr:8088")
        self.token = token

    def request(self, method: str, path: str, **kwargs):
        return super().request(method=method, path=path, _default_xml=False, **kwargs)

    def query(
            self,
            name: str,
            start_index: int,
            end_index: int
    ):
        data = self.request(
            'GET',
            '/{0}/json/SearchInfoBySubwayNameService/{1}/{2}/{3}'.format(
                self.token, start_index, end_index, name
            )
        )
        if "SearchInfoBySubwayNameService" not in data:
            raise EmptyData()
        result = data['SearchInfoBySubwayNameService']
        return [Station(x) for x in result.get("row", [])]
