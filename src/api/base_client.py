import logging
import os

import requests

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://qademo.com"


def _log_response(response, **kwargs):
    logger.info("%s %s -> %s", response.request.method, response.url, response.status_code)
    logger.info("Response body:\n%s", response.text)


class ApiClient:
    def __init__(self, base_url=None, session=None, access_token=None):
        self.base_url = (base_url or os.getenv("API_BASE_URL", DEFAULT_BASE_URL)).rstrip("/")
        self.session = session if session is not None else requests.Session()
        if access_token:
            self.session.headers["Authorization"] = f"Bearer {access_token}"
        if _log_response not in self.session.hooks["response"]:
            self.session.hooks["response"].append(_log_response)

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        return self.session.request(method, url, **kwargs)

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def patch(self, path, **kwargs):
        return self.request("PATCH", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)

    def close(self):
        self.session.close()