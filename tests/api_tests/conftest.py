from collections.abc import Generator

import pytest

from config.environments import get_standard_user
from src.api import ApiClient, AuthClient, ProductsClient, UserClient


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


@pytest.fixture
def standard_user_login_api(auth_client: AuthClient) -> UserClient:
    """Authenticate as the standard user."""
    user = get_standard_user()
    return auth_client.login(
        username=user.username,
        password=user.password,
    )