from collections.abc import Generator

import pytest

from src.api import ApiClient, AuthClient, ProductsClient, UserClient
from test_data.users import STANDARD_USER


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
    return auth_client.login(
        username=STANDARD_USER["username"],
        password=STANDARD_USER["password"],
    )