import allure

from src.api.products_client import ProductsClient


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

    with allure.step("Verify that GET /api/products endpoint returns all products"):
        response = products_client.get("/api/products")
        assert response.status_code == expected_status_code
        decoded_content = response.json()
        assert decoded_content["meta"]["total"]
