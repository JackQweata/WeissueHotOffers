import requests
from fake_headers import Headers


def response(url):
    header = Headers(headers=True)
    try:

        return requests.get(url, headers=header.generate()).json()

    except Exception as err:
        return
