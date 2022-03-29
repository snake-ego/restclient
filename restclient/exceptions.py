from httpx import TimeoutException, NetworkError

__all__ = [
    'TimeoutException',
    'NetworkError'
]


class RestQueryError(Exception):
    name: str
    code: int

    def __init__(self, name: str, code: int, *args):
        super().__init__(*args)

        self.name = name
        self.code = code

    def __str__(self):
        return f'{self.name} Error: {self.message} ({self.code})'

    @property
    def message(self):
        return "\n".join(self.args)
