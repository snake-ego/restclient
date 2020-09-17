from httpx.exceptions import TimeoutException, NetworkError

__all__ = [
    'TimeoutException',
    'NetworkError'
]


class RestQueryError(Exception):
    name: str
    code: int
    message: str

    def __init__(self, name, code, message):
        super().__init__()

        self.name = name
        self.code = code
        self.message = message

    def __str__(self):
        return f'{self.name} Error: {self.message} ({self.code})'
