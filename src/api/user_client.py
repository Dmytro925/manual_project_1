from dataclasses import dataclass
from typing import Any

import requests

from src.api.base_client import ApiClient


@dataclass(frozen=True)
class UserSession:
    """Store authenticated user data and access token."""

    user: dict[str, Any]
    access_token: str

    @property
    def username(self) -> str:
        """Return the username."""
        return self.user["username"]


class UserClient(ApiClient):
    """API client authenticated as a specific user."""

    def __init__(
        self,
        user_session: UserSession,
        base_url: str | None = None,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize the client with the user's session."""
        self.user_session = user_session
        super().__init__(
            base_url=base_url,
            session=session,
            access_token=user_session.access_token,
        )