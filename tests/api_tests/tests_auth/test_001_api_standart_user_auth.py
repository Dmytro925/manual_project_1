import requests

def test_standard_user_login_api(log_api_response, standard_user_login_api):
    """Getting an Access Token
    Endpoint: POST /api/auth/login
    Access Token: Expires in 15 minutes
    Refresh Token: Expires in 7 days"""

    assert standard_user_login_api.status_code == 200
    assert standard_user_login_api.json()["data"]["user"]["username"] == "standard_user"
    assert standard_user_login_api.json()["data"]["accessToken"]
    #assert standard_user_login_api["refreshToken"]

def test_get_all_products_api(log_api_response):
    """1. Get All Products
    Endpoint: GET /api/products
    Description: List all active products with stock information
    Auth Required: No"""

    response = requests.get(
        "https://qademo.com/api/products",
    )

    assert response.status_code == 200
    assert response.json()["meta"]["total"] == 129

