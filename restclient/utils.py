from functools import wraps
from .exceptions import RestQueryError


def proxy(fn):
    @wraps(fn)
    def proxy_query(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except RestQueryError as e:
            return e.message, e.code
    return proxy_query
