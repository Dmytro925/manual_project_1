import os
from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass(frozen=True)
class UserCredentials:



    username: str
    password: str
    type: Literal["standard", "locked", "admin"]


def _get_env(name: str) -> str:
    """Return a required environment variable or raise with an actionable message."""
    value = os.environ.get(name)
    if not value:
        msg = f"{name} is not set. Copy .env.example to .env and fill in the value."
        raise RuntimeError(msg)
    return value


def get_base_url() -> str:
    """Return the application base URL from environment variables."""
    return _get_env("BASE_URL")


def get_api_base_url() -> str:
    """Return the API base URL or fall back to the application URL."""
    return os.environ.get("API_BASE_URL") or get_base_url()


def get_standard_user() -> UserCredentials:
    """Return credentials for the standard user."""
    return UserCredentials(
        username=_get_env("STANDARD_USER_USERNAME"),
        password=_get_env("STANDARD_USER_PASSWORD"),
        type="standard",
    )


def get_locked_user() -> UserCredentials:
    """Return credentials for the locked user."""
    return UserCredentials(
        username=_get_env("LOCKED_USER_USERNAME"),
        password=_get_env("LOCKED_USER_PASSWORD"),
        type="locked",
    )


def get_admin_user() -> UserCredentials:
    """Return admin credentials with the password generated for today's date."""
    template = _get_env("ADMIN_USER_PASSWORD_TEMPLATE")
    return UserCredentials(
        username=_get_env("ADMIN_USER_USERNAME"),
        password=template.format(date=datetime.now().strftime("%d%m%Y")),
        type="admin",
    )
