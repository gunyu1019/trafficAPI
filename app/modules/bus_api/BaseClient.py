import json
import xmltodict

from abc import *
from typing import Dict, Any, Optional
from requests import request
from bs4 import BeautifulSoup


class BaseClient(metaclass=ABCMeta):
    def __init__(self, base_url: str):
        self.BASE = base_url

    def request(
            self,
            method: str,
            path: str,
            _default_params: Dict[str, Any],
            _default_xml: bool = False,
            **kwargs
    ):
        url = "{0}{1}".format(self.BASE, path)

        params = _default_params
        if "params" not in kwargs:
            kwargs['params'] = params
        else:
            kwargs['params'].update(params)

        response = request(
            method, url, **kwargs
        )

        if response.headers.get("Content-Type").startswith("application/json"):
            result = response.json()
        elif response.headers.get("Content-Type").startswith("application/xml"):
            result = xmltodict.parse(response.text)
        else:
            result = response.text
            if not _default_xml:
                result = json.loads(result)
            else:
                print(result)
                result = xmltodict.parse(response.text)

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
