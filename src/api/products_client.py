from src.api.base_client import ApiClient


class ProductsClient(ApiClient):
    def get_all(self):
        return self.get("/api/products")

    def get_product_by_name(self, product_name):
        return self.get_by_name(f"/api/products/{product_name}")