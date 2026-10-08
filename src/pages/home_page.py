from playwright.sync_api import Page
from pages.base_page import BasePage

class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.page.goto("https://qademo.com/")