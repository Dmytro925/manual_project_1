import requests

def test_standard_user_login_api(standard_user_login_api):
    """Getting an Access Token
    Endpoint: POST /api/auth/login
    Access Token: Expires in 15 minutes
    Refresh Token: Expires in 7 days"""

    assert standard_user_login_api.user_session.username == "standard_user"
    assert standard_user_login_api.user_session.access_token

def test_get_all_products_api(product_client):
    """1. Get All Products
    Endpoint: GET /api/products
    Description: List all active products with stock information
    Auth Required: No"""

    response = product_client.get_all_products()

    assert response.status_code == 200
    assert response.json()["meta"]["total"] == 129

