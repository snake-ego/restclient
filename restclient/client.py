import httpx
from json import dumps

from .exceptions import RestQueryError, TimeoutException, NetworkError
from .structures import RestErrors
from .response import RestResponse, ErrorResponse
from .headers import RestHeaders
from .urls import RestURL

__all__ = ['RestClient']


class BaseRestClient:
    name: str

    def __init__(self, address=None, endpoints=None, headers=None, strict=False, **kwargs):
        self.url = RestURL(address, endpoints=endpoints, strict=strict)
        self.headers = RestHeaders(**headers) if isinstance(headers, dict) else RestHeaders()
        self.full_response = self._extract_full_response(kwargs.get('full_response'))

    def _extract_headers(self, headers=None):
        if isinstance(headers, dict):
            return headers

        return {}

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


class RestClient(BaseRestClient):
    name: str

    def __call__(self, method, *address, ok_codes=None, full_response=None, **kwargs):
        if len(address) == 0:
            raise ValueError("Address not set")

        ok_codes = self._extract_codes(ok_codes)
        full_response = self._extract_full_response(full_response)

        query = {
            'url': self.url(*address, **kwargs.pop('params', {})),
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

    def send(self, method, url, *args, **kwargs):
        try:
            return RestResponse(httpx.request(method, url, *args, **kwargs))
        except NetworkError:
            return RestResponse(ErrorResponse(url, **RestErrors.refused))
        except TimeoutException:
            return RestResponse(ErrorResponse(url, **RestErrors.timeout))


class AsyncRestClient(BaseRestClient):
    name: str

    async def __call__(self, method, *address, ok_codes=None, full_response=None, **kwargs):
        if len(address) == 0:
            raise ValueError("Address not set")

        ok_codes = self._extract_codes(ok_codes)
        full_response = self._extract_full_response(full_response)

        query = {
            'url': self.url(*address, **kwargs.pop('params', {})),
            'headers': self.headers(**self._extract_headers(kwargs.pop('headers', None))),
            'data': self._extract_data(kwargs.pop('data', None), kwargs.pop('json', None)),
            **kwargs
        }
        if 'timeout' in kwargs:
            query.update(timeout=kwargs['timeout'])

        response = await self.send(method.upper(), **query)

        if not response.is_ok(ok_codes):
            name = self.name if hasattr(self, 'name') else type(self).__name__
            raise RestQueryError(name, response.status_code, response.content)

        if full_response or int(response.headers.get('Content-Length', '0')) <= 1:
            return response
        return response.content

    async def send(self, method, url, *args, **kwargs):
        try:
            async with httpx.AsyncClient() as client:
                return RestResponse(await client.request(method, url, *args, **kwargs))
        except NetworkError:
            return RestResponse(ErrorResponse(url, **RestErrors.refused))
        except TimeoutException:
            return RestResponse(ErrorResponse(url, **RestErrors.timeout))
