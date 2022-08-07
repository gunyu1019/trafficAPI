from app.modules.baseClient import BaseClient
from app.modules.errors import EmptyData
from typing import Optional, Tuple
from .rideBike import RideBike


class Client(BaseClient):
    def __init__(self, token: str):
        super(Client, self).__init__("http://openapi.seoul.go.kr:8088")
        self.token = token

    async def request(self, method: str, path: str, **kwargs):
        return await super().request(method=method, path=path, _default_xml=False, **kwargs)

    async def bike_list(
            self,
            start_index: int,
            end_index: int
    ):
        data = await self.request(
            'GET',
            '/{0}/json/bikeList/{1}/{2}'.format(
                self.token, start_index, end_index
            )
        )
        if "rentBikeStatus" not in data:
            raise EmptyData()
        result = data['rentBikeStatus']
        return [RideBike(x) for x in result.get("row", [])]
