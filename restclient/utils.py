def trim(url: str) -> str:
    if url[0] == "/":
        url = url[1:]
    if url[-1] == "/":
        url = url[:-1]
    return url
