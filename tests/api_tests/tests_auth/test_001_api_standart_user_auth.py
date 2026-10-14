from src.api.products_client import ProductsClient
from src.api.user_client import UserClient


def test_standard_user_login_api(standard_user_login_api: UserClient) -> None:
    """Getting an Access Token
    Endpoint: POST /api/auth/login
    Access Token: Expires in 15 minutes
    Refresh Token: Expires in 7 days"""

    assert standard_user_login_api.user_session.username == "standard_user"
    assert standard_user_login_api.user_session.access_token

def test_get_all_products_api(products_client: ProductsClient) -> None:
    """1. Get All Products
    Endpoint: GET /api/products
    Description: List all active products with stock information
    Auth Required: No"""

    response = products_client.get_all()

    assert response.status_code == 200
    assert response.json()["meta"]["total"] > 10

