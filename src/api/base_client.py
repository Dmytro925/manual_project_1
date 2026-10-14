import logging
import os
from typing import Any

import requests
from requests import Response
from requests.sessions import Session

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://qademo.com"


def _log_response(response: Response, **kwargs: object) -> None:
    """Log the HTTP response status and body."""
    logger.info(
        "%s %s -> %s",
        response.request.method,
        response.url,
        response.status_code,
    )
    logger.info("Response body:\n%s", response.text)


class ApiClient:
    """Base HTTP client for API requests."""

    def __init__(
        self,
        base_url: str | None = None,
        session: Session | None = None,
        access_token: str | None = None,
    ) -> None:
        self.base_url = (
            base_url or os.getenv("API_BASE_URL", DEFAULT_BASE_URL)
        ).rstrip("/")
        self.session = session if session is not None else requests.Session()

        if access_token:
            self.session.headers["Authorization"] = f"Bearer {access_token}"

        if _log_response not in self.session.hooks["response"]:
            self.session.hooks["response"].append(_log_response)

    def request(
        self,
        method: str,
        path: str,
        **kwargs: Any,  # noqa: ANN401
    ) -> Response:
        """Send an HTTP request."""
        url = f"{self.base_url}{path}"
        return self.session.request(method, url, **kwargs)

    def get(self, path: str, **kwargs: Any) -> Response:  # noqa: ANN401
        """Send a GET request."""
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:  # noqa: ANN401
        """Send a POST request."""
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:  # noqa: ANN401
        """Send a PUT request."""
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Response:  # noqa: ANN401
        """Send a PATCH request."""
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:  # noqa: ANN401
        """Send a DELETE request."""
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()