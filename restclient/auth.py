from __future__ import annotations
import typing as t

from httpx.auth import Auth, BasicAuth
from httpx.models import Request, Response

__all__ = [
    'BasicAuth'
]


class TokenAuth(Auth):
    """ Allows the 'auth' argument to be passed as a token, and uses HTTP Bearer authentication. """

    def __init__(self, token: str):
        self.auth_header = f"Bearer {token}"

    def auth_flow(self, request: Request) -> t.Generator[Request, Response, None]:
        request.headers["Authorization"] = self.auth_header
        yield request
