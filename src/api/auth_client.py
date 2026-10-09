from src.api.base_client import ApiClient
from src.api.user_client import UserClient, UserSession


class AuthError(Exception):
    pass


class AuthClient(ApiClient):
    def login(self, username, password):
        response = self.post(
            "/api/auth/login",
            json={"username": username, "password": password},
        )
        if response.status_code != 200:
            raise AuthError(f"Login failed: {response.status_code} {response.text}")

        data = response.json()["data"]
        user_session = UserSession(
            user=data["user"],
            access_token=data["accessToken"]
        )
        return UserClient(
            user_session=user_session,
            base_url=self.base_url,
            session=self.session,
        )