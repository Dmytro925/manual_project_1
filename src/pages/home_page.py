from playwright.sync_api import Page
from src.pages import BasePage

class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.page.goto("https://qademo.com/")