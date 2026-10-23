from playwright.sync_api import Page

from src.pages.base_page import BasePage


class CatalogPage(BasePage):
    """Page object for the product catalog."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.add_to_cart_button = page.get_by_role(
            "button", name="Add Laptop Backpack to cart"
        )

    def open(self) -> None:
        """Open the catalog page."""

        self.page.goto("/catalog")
