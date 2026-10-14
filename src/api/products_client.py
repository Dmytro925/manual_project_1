from requests import Response

from src.api.base_client import ApiClient


class ProductsClient(ApiClient):
    """Client for products API endpoints."""

    def get_all(self) -> Response:
        """Get all products."""
        return self.get("/api/products")

    def get_product_by_name(self, product_name: str) -> Response:
        """Get a product by its name."""
        return self.get(f"/api/products/{product_name}")