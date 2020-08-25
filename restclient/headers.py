from __future__ import annotations
import typing as t

from .structures import Header


class RestHeaders(object):
    __headers__: t.List[Header]

    def __init__(self, *args, **kwargs):
        self.__headers__ = self.create(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        result = {}

        for header in self.__headers__:
            result.update(header.to_dict())
        for header in self.create(*args, **kwargs):
            result.update(header.to_dict())

        return result

    def create(self, *args, **kwargs) -> t.List[Header]:
        result = Header.parse(kwargs)
        for header in args:
            result.extend(Header.parse(header))
        return result

    def has(self, name) -> bool:
        return any(filter(lambda h: t.cast(Header, h).name == name.lower(), self.__headers__))

    def keys(self) -> t.List[str]:
        return [h.name for h in self.__headers__]

    def get(self, name: str, default: str = None) -> t.Optional[str]:
        if (result := next(filter(lambda h: t.cast(Header, h).name == name.lower(), self.__headers__), None)) is None:
            return default
        return result.value

    def __getitem__(self, name: str) -> str:
        if (result := self.get(name, None)) is None:
            raise KeyError(name)
        return result
