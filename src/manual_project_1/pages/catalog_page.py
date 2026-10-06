from playwright.sync_api import Page
from manual_project_1.pages.base_page import BasePage

class CatalogPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.add_to_cart_button = page.get_by_role(
            "button",
            name="Add Laptop Backpack to cart"
        )

    def open(self):
        self.page.goto("https://qademo.com/catalog")