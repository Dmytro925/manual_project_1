from playwright.sync_api import Page
from src.pages.shared_components.nawbar import Navbar

class BasePage(Page):
    def __init__(self, page: Page):
        self.page = page
        self.navbar = Navbar(page)

