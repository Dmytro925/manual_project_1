from src.api.base_client import ApiClient


class ProductsClient(ApiClient):
    def get_all_products(self):
        return self.get("/api/products")

    def get_product(self, product_id):
        return self.get(f"/api/products/{product_id}")