from dataclasses import dataclass

from src.api.base_client import ApiClient


@dataclass(frozen=True)
class UserSession:
    user: dict
    access_token: str

    @property
    def username(self):
        return self.user["username"]


class UserClient(ApiClient):
    def __init__(self, user_session, base_url=None, session=None):
        super().__init__(
            base_url=base_url,
            session=session,
            access_token=user_session.access_token,
        )
        self.user_session = user_session