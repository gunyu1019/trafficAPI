import asyncio
import json
import aiohttp
import xmltodict

from typing import Dict, Any


class BaseClient:
    def __init__(
            self,
            base_url: str,
            loop: asyncio.AbstractEventLoop = None
    ):
        self.BASE = base_url
        self.loop = loop or asyncio.get_event_loop()

    async def request(
            self,
            method: str,
            path: str,
            convert_type: bool = True,
            session: aiohttp.ClientSession = None,
            _default_params: Dict[str, Any] = None,
            _default_xml: bool = False,
            **kwargs
    ):
        if _default_params is None:
            _default_params = {}
        url = "{0}{1}".format(self.BASE, path)

        is_single = False
        if session is None:
            is_single = True
            session = aiohttp.ClientSession()

        params = _default_params
        if "params" not in kwargs:
            kwargs['params'] = params
        else:
            kwargs['params'].update(params)

        response = await session.request(
            method, url, **kwargs
        )

        if not convert_type:
            response.close()
            if is_single:
                await session.close()
            return await response.text()

        if response.headers.get("Content-Type").startswith("application/json"):
            result = await response.json()
        elif (
                response.headers.get("Content-Type").startswith("application/xml") or
                response.headers.get("Content-Type").startswith("text/xml")
        ):
            _text = await response.text('utf-8')
            result = xmltodict.parse(_text)
        else:
            _text = await response.text('utf-8')
            if not _default_xml:
                result = json.loads(_text)
            else:
                result = xmltodict.parse(_text)

        response.close()
        if is_single:
            await session.close()
        return result

    async def get(self, path: str, **kwargs):
        return await self.request(
            method="GET",
            path=path,
            **kwargs
        )

    async def post(self, path: str, **kwargs):
        return await self.request(
            method="POST",
            path=path,
            **kwargs
        )
