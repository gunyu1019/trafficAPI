from app.modules.baseClient import BaseClient
from app.modules.errors import EmptyData
from .realtimeArrival import RealtimeArrival


class Arrival(BaseClient):
    def __init__(self, token: str):
        super().__init__("http://swopenapi.seoul.go.kr")
        self.token = token

    async def request(self, method: str, path: str, **kwargs):
        return await super().request(method=method, path=path, _default_xml=False, **kwargs)

    async def arrival_info(
            self,
            name: str,
            start_index: int,
            end_index: int
    ):
        data = await self.request(
            'GET',
            '/api/subway/{0}/json/realtimeStationArrival/{1}/{2}/{3}'.format(
                self.token, start_index, end_index, name
            )
        )
        if "realtimeArrivalList" not in data:
            raise EmptyData()
        result = data['realtimeArrivalList']
        return [RealtimeArrival.from_payload(x) for x in result]
