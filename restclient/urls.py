from __future__ import annotations
import typing as t

from .structures import Endpoint
from .utils import trim
from .constants import HTTP_PATTERN


class RestURL:
    strict: bool
    address: str = ''

    endpoints: t.List[Endpoint]

    def __init__(self,
                 address: str = None,
                 *,
                 endpoints: t.Union[t.Dict[str, str], t.List[str], t.Tuple[str, str], str] = None,
                 strict: bool = False):
        self.strict = strict
        self.endpoints = Endpoint.parse(endpoints)
        if self.is_valid_url(address):
            self.address = trim(address)

    def __call__(self, address: str, *uri_params: t.Union[str, int], **kwargs: t.Union[str, int]) -> str:
        if not self.is_valid_url(address):
            address = self.url_for(address, *uri_params)
        return self.set_params(address, **kwargs)

    def is_valid_url(self, url: str) -> bool:
        if not isinstance(url, str):
            return False
        return bool(HTTP_PATTERN.match(url))

    def url_for(self, endpoint: str, *uri_params: t.Union[str, int]) -> str:
        target = self.get_endpoint(endpoint).uri.format(*uri_params)
        if self.is_valid_url(target):
            return target

        query = [self.address, target]
        if not self.strict:
            query.append("")

        return "/".join(query)

    def set_params(self, url: str, **params: t.Union[str, int]) -> str:
        if not params:
            return url
        return f"{url}?{'&'.join(['{}={}'.format(*i) for i in params.items()])}"

    def has_endpoint(self, name: str) -> bool:
        return any(filter(lambda e: e.name == name, self.endpoints))

    def get_endpoint(self, name: str) -> Endpoint:
        if (result := next(filter(lambda e: e.name == name, self.endpoints), None)) is None:
            raise ValueError(f"Endpoint '{name}' doesn't exists")
        return result
