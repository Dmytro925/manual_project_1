from playwright.sync_api import Page

from src.pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for the home page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        """Open the home page."""

        self.page.goto("/")