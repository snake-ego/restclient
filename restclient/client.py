import typing as t
import requests
import re

from json import dumps

from .exceptions import RestQueryError
from .response import RestResponse, ErrorResponse
from .structs import RestErrors
from .headers import RestHeaders

__all__ = ['RestClient']


class RestURL(object):
    strict: bool
    url: str

    _endpoints: t.Dict[str, str]
    _pattern = re.compile("^https?://.+")

    def __init__(self, address=None, endpoints=None, strict=False):
        self.strict = strict
        self.url = self.trim(address) if self.is_valid_url(address) else ''
        self._endpoints = dict()

        if isinstance(endpoints, (list, tuple)):
            self.endpoints(*endpoints)
        elif isinstance(endpoints, dict):
            self.endpoints(**endpoints)
        else:
            self.endpoints(endpoints)

    def __call__(self, address, *fmt, **kwargs) -> str:
        if not self.is_valid_url(address):
            address = self.url_for(address, *fmt)

        return self.set_params(address, **kwargs)

    def is_valid_url(self, url: str) -> bool:
        if not isinstance(url, str):
            return False

        return bool(self._pattern.match(url))

    def set_params(self, url, **params) -> str:
        if not params:
            return url

        return url + "?" + "&".join(["{}={}".format(*i)
                                     for i in params.items()])

    def url_for(self, endpoint, *fmt) -> str:
        if not self.is_endpoint(endpoint):
            raise ValueError("Endpoint '{}' doesn't exists".format(endpoint))

        e = self._endpoints.get(endpoint, '').format(*fmt)
        if self.is_valid_url(e):
            return e

        query = [self.url, e]
        if not self.strict:
            query.append("")

        return "/".join(query)

    def endpoints(self, *args, **kwargs):
        [self._endpoints.update(self._parse_endpoint(h)) for h in args]
        self._endpoints.update(kwargs)
        return self

    def _parse_endpoint(self, endpoint) -> dict:
        if isinstance(endpoint, dict):
            return {k: self.trim(v) for k, v in endpoint.items()}

        if isinstance(endpoint, (tuple, list)) and len(endpoint) == 2:
            return {k: self.trim(v) for k, v in endpoint}

        if isinstance(endpoint, str):
            return {endpoint: endpoint}

        return dict()

    def is_endpoint(self, item: str) -> bool:
        return self.trim(item) in self._endpoints

    def trim(self, url: str) -> str:
        url = url[1:] if url[0] == "/" else url
        url = url[: -1] if url[-1] == "/" else url
        return url


class RestClient(object):
    def __init__(self, address=None, endpoints=None, headers=None, strict=False, **kwargs):
        self.url = RestURL(address, endpoints, strict)
        self.headers = RestHeaders(**headers) if isinstance(headers, dict) else RestHeaders()
        self.full_response = self._extract_full_response(kwargs.get('full_response'))

    def __call__(self, method, *address, ok_codes=None, full_response=None, **kwargs):
        if len(address) == 0:
            raise ValueError("Address not set")

        ok_codes = self._extract_codes(ok_codes)
        full_response = self._extract_full_response(full_response)

        query = {
            'url': self.url(*address, **kwargs.pop('params', dict())),
            'headers': self.headers(**self._extract_headers(kwargs.pop('headers', None))),
            'data': self._extract_data(kwargs.pop('data', None), kwargs.pop('json', None)),
            **kwargs
        }
        if 'timeout' in kwargs:
            query.update(timeout=kwargs['timeout'])

        response = self.send(method.upper(), **query)

        if not response.is_ok(ok_codes):
            name = self.name if hasattr(self, 'name') else type(self).__name__
            raise RestQueryError(name, response.status_code, response.content)

        if full_response or int(response.headers.get('Content-Length', '0')) <= 1:
            return response
        return response.content

    def _extract_headers(self, headers=None):
        if isinstance(headers, dict):
            return headers

        return dict()

    def _extract_codes(self, code=None) -> list:
        if isinstance(code, int):
            return [code]
        if isinstance(code, (list, tuple)):
            return list(code)
        return [200]

    def _extract_full_response(self, full_response=None):
        if isinstance(full_response, bool):
            return full_response

        return getattr(self, 'full_response', False)

    def _extract_data(self, data=None, json=None):
        if data is None and json is not None:
            data = dumps(json)
        return data

    def send(self, method, url, *args, **kwargs):
        try:
            return RestResponse(requests.request(method, url, *args, **kwargs))
        except requests.ConnectionError:
            return RestResponse(ErrorResponse(url, **RestErrors.refused))
        except requests.Timeout:
            return RestResponse(ErrorResponse(url, **RestErrors.timeout))
