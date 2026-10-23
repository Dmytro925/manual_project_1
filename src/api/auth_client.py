from requests import Response

from src.api.base_client import ApiClient
from src.api.user_client import UserClient, UserSession


class AuthError(Exception):
    """Raised when authentication fails."""


class AuthClient(ApiClient):
    """Client for authentication API endpoints."""

    def login(self, username: str, password: str) -> UserClient:
        """Authenticate a user and return an authenticated API client."""
        response: Response = self.post(
            "/api/auth/login",
            json={"username": username, "password": password},
        )

        if response.status_code != 200:
            raise AuthError(f"Login failed: {response.status_code} {response.text}")

        data = response.json()["data"]
        user_session = UserSession(
            user=data["user"],
            access_token=data["accessToken"],
        )

        return UserClient(
            user_session=user_session,
            base_url=self.base_url,
            session=self.session,
        )
