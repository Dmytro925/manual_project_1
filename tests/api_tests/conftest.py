import pytest
import requests
from test_data.users import STANDARD_USER
from src.api.base_client import ApiClient
from src.api.products_client import ProductsClient
from src.api.auth_client import AuthClient

@pytest.fixture()
def api_client():
    client = ApiClient()
    yield client
    client.close()

@pytest.fixture()
def products_client():
    client = ProductsClient()
    yield client
    client.close()

@pytest.fixture()
def auth_client():
    client = AuthClient()
    yield client
    client.close()

@pytest.fixture
def standard_user_login_api(auth_client):
    return auth_client.login(
        username=STANDARD_USER["username"],
        password=STANDARD_USER["password"],
    )