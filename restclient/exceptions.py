class RestQueryError(Exception):
    def __init__(self, name, code, message):
        self.name = name
        self.code = code
        self.message = message

    def __str__(self):
        return f'{self.name} Error: {self.message} ({self.code})'
