import os
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UserCredentials:
    """Store credentials and the user's account type."""

    username: str
    password: str
    type: str


def get_base_url() -> str:
    """Return the application base URL from environment variables."""
    return os.environ["BASE_URL"]


def get_api_base_url() -> str:
    """Return the API base URL or fall back to the application URL."""
    return os.environ.get("API_BASE_URL") or get_base_url()


def get_standard_user() -> UserCredentials:
    """Return credentials for the standard user."""
    return UserCredentials(
        username=os.environ["STANDARD_USER_USERNAME"],
        password=os.environ["STANDARD_USER_PASSWORD"],
        type="standard",
    )


def get_locked_user() -> UserCredentials:
    """Return credentials for the locked user."""
    return UserCredentials(
        username=os.environ["LOCKED_USER_USERNAME"],
        password=os.environ["LOCKED_USER_PASSWORD"],
        type="locked",
    )


def get_admin_user() -> UserCredentials:
    """Return admin credentials with the password generated for today's date."""
    template = os.environ["ADMIN_USER_PASSWORD_TEMPLATE"]
    return UserCredentials(
        username=os.environ["ADMIN_USER_USERNAME"],
        password=template.format(date=datetime.now().strftime("%d%m%Y")),
        type="admin",
    )
