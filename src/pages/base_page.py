from playwright.sync_api import Page

from src.pages.shared_components.nawbar import Navbar


class BasePage(Page):
    """Base page providing shared page functionality."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.navbar = Navbar(page)
