from __future__ import annotations
import typing as t

from dataclasses import dataclass

from .utils import trim


class RestErrors:
    refused = dict(status_code=1, text='Connection Refused')
    timeout = dict(status_code=1, text='Connection Timeout')


@dataclass
class Endpoint:
    name: str
    uri: str

    @classmethod
    def create(cls, name: str, uri: str) -> Endpoint:
        return cls(name=name, uri=trim(uri))

    @classmethod
    def parse(cls, endpoint: t.Union[t.Dict[str, str], t.List[str], t.Tuple[str, str], str]) -> t.List[Endpoint]:
        if isinstance(endpoint, dict):
            return [cls.create(k, v) for k, v in endpoint.items()]
        if isinstance(endpoint, (tuple, list)) and len(endpoint) == 2:
            return [cls.create(k, v) for k, v in endpoint]
        if isinstance(endpoint, str):
            return [cls.create(endpoint, endpoint)]
        return []


@dataclass
class Header:
    name: str
    display: str
    value: str

    @classmethod
    def create(cls, display: str, value: str) -> Header:
        return cls(
            name=display.lower(),
            display=display,
            value=value
        )

    @classmethod
    def parse(cls, header: t.Union[t.Dict[str, str], t.List[str], t.Tuple[str, str]]) -> t.List[Header]:
        if isinstance(header, dict):
            return [Header.create(k, v) for k, v in header.items()]
        if isinstance(header, (tuple, list)) and len(header) == 2:
            return [Header.create(k, v) for k, v in header]
        return []

    def to_dict(self) -> t.Dict[str, str]:
        return {self.display: self.value}
