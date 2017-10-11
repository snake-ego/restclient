class RestHeaders(object):
    _items = dict()
    _index = dict()

    def __init__(self, **headers):
        self.add(**headers)

    def __call__(self, **headers):
        out = self._items.copy()
        out.update(**headers)
        return out

    def add(self, *args, **kwargs):
        [self._items.update(self._parse(h)) for h in args]
        self._items.update(kwargs)
        return self._reindex()

    def _parse(self, header) -> dict:
        if isinstance(header, dict):
            return header

        if isinstance(header, (tuple, list)) and len(header) == 2:
            return dict(*tuple(header))

        return dict()

    def _reindex(self):
        self._index = {k.lower(): v for k, v in self._items.items()}
        return self

    def has(self, name):
        return name.lower() in self._index.keys()

    def all(self):
        return self._items.copy()

    def get(self, key, default=None):
        return self._index.get(key.lower(), default)
