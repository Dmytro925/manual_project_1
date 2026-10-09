import pytest
import requests
from test_data.users import STANDARD_USER
from src.api.base_client import ApiClient
from src.api.product_client import ProductsClient
from src.api.auth_client import AuthClient

@pytest.fixture
def api_client():
    return ApiClient()

@pytest.fixture
def product_client(api_client):
    return ProductsClient()

@pytest.fixture
def auth_client(api_client):
    return AuthClient()

@pytest.fixture
def standard_user_login_api(auth_client):
    return auth_client.login(
        username=STANDARD_USER["username"],
        password=STANDARD_USER["password"],
    )