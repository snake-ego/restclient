from __future__ import annotations
import typing as t

from .structures import Endpoint
from .utils import trim
from .constants import HTTP_PATTERN

TEndpoint = t.Union[t.Dict[str, str], t.List[str], t.Tuple[str, str], str]


class RestURL:
    strict: bool
    address: str = ''

    __endpoints__: t.List[Endpoint]

    def __init__(self, address: str = None, *, endpoints: TEndpoint = None, strict: bool = False):
        self.strict = strict
        self.__endpoints__ = Endpoint.parse(endpoints)
        if self.is_valid_url(address):
            self.address = trim(t.cast(str, address))

    def __call__(self, address: str, *uri_params: t.Union[str, int], **kwargs: t.Union[str, int]) -> str:
        if not self.is_valid_url(address):
            address = self.url_for(address, *uri_params)
        return self.set_params(address, **kwargs)

    @staticmethod
    def set_params(url: str, **params: t.Union[str, int]) -> str:
        if not params:
            return url
        return f"{url}?{'&'.join(['{}={}'.format(*i) for i in params.items()])}"

    def url_for(self, endpoint: str, *uri_params: t.Union[str, int]) -> str:
        target = self.get_endpoint(endpoint).uri.format(*uri_params)
        if self.is_valid_url(target):
            return target

        query = [self.address, target]
        if not self.strict:
            query.append("")

        return "/".join(query)

    @staticmethod
    def is_valid_url(url: t.Optional[str]) -> bool:
        if not isinstance(url, str):
            return False
        return bool(HTTP_PATTERN.match(url))

    def has_endpoint(self, name: str) -> bool:
        return any(self._find(name))

    def get_endpoint(self, name: str) -> Endpoint:
        if (result := next(self._find(name), None)) is None:
            raise ValueError(f"Endpoint '{name}' doesn't exists")
        return result

    def add_endpoints(self, endpoints: TEndpoint) -> None:
        for endpoint in Endpoint.parse(endpoints):
            if (matched := next(self._find(endpoint.name), None)) is None:
                return self.__endpoints__.append(endpoint)
            matched.uri = endpoint.uri
        return None

    def _find(self, name: str):
        return filter(lambda e: t.cast(Endpoint, e).name == name, self.__endpoints__)
