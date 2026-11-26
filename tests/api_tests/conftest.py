import uuid
from collections.abc import Generator
from dataclasses import dataclass

import pytest

from config.environments import get_standard_user
from src.api import ApiClient, AuthClient, ProductsClient, UserClient

# Fixture-local values for throwaway signups, not environment credentials.
DISPOSABLE_ACCOUNT_PASSWORD = "NewUser1!"
DISPOSABLE_ACCOUNT_PHONE = "380501234567"


@dataclass(frozen=True)
class DisposableAccount:
    """A throwaway standard account created for a test."""

    username: str
    email: str
    password: str


@pytest.fixture()
def api_client() -> Generator[ApiClient]:
    """Provide an API client."""
    client = ApiClient()
    yield client
    client.close()


@pytest.fixture()
def products_client() -> Generator[ProductsClient]:
    """Provide a products API client."""
    client = ProductsClient()
    yield client
    client.close()


@pytest.fixture()
def auth_client() -> Generator[AuthClient]:
    """Provide an authentication API client."""
    client = AuthClient()
    yield client
    client.close()


@pytest.fixture()
def disposable_account(auth_client: AuthClient) -> DisposableAccount:
    """Create a disposable standard account through the signup endpoint."""
    email = f"qa.{uuid.uuid4().hex}@mailinator.com"
    user_client = auth_client.signup(
        email=email,
        phone=DISPOSABLE_ACCOUNT_PHONE,
        password=DISPOSABLE_ACCOUNT_PASSWORD,
    )
    return DisposableAccount(
        username=user_client.user_session.username,
        email=email,
        password=DISPOSABLE_ACCOUNT_PASSWORD,
    )


@pytest.fixture
def standard_user_login_api(auth_client: AuthClient) -> UserClient:
    """Authenticate as the standard user."""
    user = get_standard_user()
    return auth_client.login(
        username=user.username,
        password=user.password,
    )
