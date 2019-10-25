import requests
from json import dumps
from abc import ABC, abstractmethod, abstractproperty

from .headers import RestHeaders


class BaseResponse(ABC):

    @abstractmethod
    def json(self):
        raise NotImplementedError()

    @abstractproperty
    def text(self):
        raise NotImplementedError()


class RestResponse(BaseResponse):
    _raw = None

    def __init__(self, response):
        self._raw = response

        if not isinstance(response, (requests.Response, ErrorResponse)):
            raise ValueError(
                'Responce argument must be instance of {}'.format(
                    requests.Response))

        self._headers = RestHeaders(**response.headers)

    def is_ok(self, codes):
        if self.status_code in codes:
            return True

        return False

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, value):
        return

    @property
    def status_code(self):
        return self._raw.status_code

    @property
    def content(self):
        if self.headers.get('content-type', '').find('application/json') != -1:
            return self.json()

        return self._raw.text

    @property
    def url(self):
        return self._raw.url

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        return

    def json(self):
        return self._raw.json()

    @property
    def text(self):
        return self.raw._text


class ErrorResponse(BaseResponse):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.headers = RestHeaders(**kwargs.get('headers', {}))
        self.status_code = kwargs.get('status_code', None)
        self._text = kwargs.get('text', None)
        self._json = kwargs.get('json', None)

    def json(self):
        if self._json is not None:
            return self._json

        return dumps(self._text)

    @property
    def text(self):
        return self._text
