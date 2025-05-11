from typing import Optional

import requests
from requests.auth import HTTPBasicAuth


def default_on_response(response: requests.Response) -> Optional[dict]:
    """
    :param response:
    :return: the input response
    :raise HTTPError: if status_code is not OK(200)
    """
    if response.status_code != 200:
        response.raise_for_status()
    else:
        return response.json()


class Request:
    def __init__(self, url: str, auth: dict = None, on_response=default_on_response):
        self.url = url
        self.options: dict = {
            'headers': {}
        }
        if auth is not None:
            bearer = auth.get('bearer')
            if bearer is not None:
                self.options['headers']['Authorization'] = f"Bearer {bearer}"
                del auth['bearer']
            else:
                self.options['auth'] = HTTPBasicAuth(auth['username'], auth['password'])
        self.on_response = on_response

    def get(self, params=None) -> dict:

        response = requests.get(self.url, params, **self.options)
        return self.on_response(response)

    def post(self, json=None, data=None) -> dict:

        response = requests.post(self.url, data, json, **self.options)
        return self.on_response(response)
