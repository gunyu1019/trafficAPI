import json
import xmltodict

from typing import Dict, Any
from requests import request


class BaseClient:
    def __init__(self, base_url: str):
        self.BASE = base_url

    def request(
            self,
            method: str,
            path: str,
            _default_params: Dict[str, Any] = None,
            converted: bool = True,
            _default_xml: bool = False,
            **kwargs
    ):
        if _default_params is None:
            _default_params = {}
        url = "{0}{1}".format(self.BASE, path)

        params = _default_params
        if "params" not in kwargs:
            kwargs['params'] = params
        else:
            kwargs['params'].update(params)

        response = request(
            method, url, **kwargs
        )

        if not converted:
            return response.text

        if response.headers.get("Content-Type").startswith("application/json"):
            result = response.json()
        elif (
                response.headers.get("Content-Type").startswith("application/xml") or
                response.headers.get("Content-Type").startswith("text/xml")
        ):
            result = xmltodict.parse(response.content.decode('utf-8'))
        else:
            result = response.text
            if not _default_xml:
                result = json.loads(result)
            else:
                result = xmltodict.parse(response.content.decode('utf-8'))
        return result

    def get(self, path: str, **kwargs):
        return self.request(
            method="GET",
            path=path,
            **kwargs
        )

    def post(self, path: str, **kwargs):
        return self.request(
            method="POST",
            path=path,
            **kwargs
        )
