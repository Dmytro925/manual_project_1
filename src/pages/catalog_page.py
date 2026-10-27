from playwright.sync_api import Page

from src.pages.base_page import BasePage


class CatalogPage(BasePage):
    """Page object for the product catalog."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def add_to_cart(self, product_name: str) -> None:
        """Add a product to the cart."""
        self.page.get_by_role("button", name=f"Add {product_name} to cart").click()

    def open(self) -> None:
        """Open the catalog page."""

        self.page.goto("/catalog")
