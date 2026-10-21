import allure

from src.api import ProductsClient, UserClient


@allure.id("FR_AUTH_002")
@allure.epic("Authentication API")
@allure.feature("Login Page (/login)")
@allure.story("POST /api/auth/login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Standard user login API")
def test_standard_user_login_api(standard_user_login_api: UserClient):
    """Getting an Access Token
    Endpoint: POST /api/auth/login
    Access Token: Expires in 15 minutes
    Refresh Token: Expires in 7 days"""

    with allure.step("Verify that standard_user is shown in navbar after login"):
        assert standard_user_login_api.user_session.username == "standard_user"
        assert standard_user_login_api.user_session.access_token

@allure.id("FR-PROD-003")
@allure.epic("Public endpoints API")
@allure.feature("Get All Products")
@allure.story("GET /api/products")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("List all active products with stock information")
def test_get_all_products_api(products_client: ProductsClient):
    """1. Get All Products
    Endpoint: GET /api/products
    Description: List all active products with stock information
    Auth Required: No"""
    expected_status_code = 200
    expected_product_number = 10

    with allure.step("Verify that GET /api/products endpoint returns all products"):
        response = products_client.get_all()
        assert response.status_code == expected_status_code
        assert response.json()["meta"]["total"] > expected_product_number