from playwright.sync_api import Page
from manual_project_1.pages.base_page import BasePage

class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.email_input = page.get_by_label("email")
        self.password_input = page.get_by_label("password")
        self.login_button = page.get_by_test_id("login-submit-button")
        self.back_home_link = page.get_by_test_id("back-to-home-link")
        self.create_account_link = page.get_by_test_id("sign-up-link")
        self.username_field = page.get_by_label("username")
        self.password_field = page.get_by_label("password")
        self.login_error_message = page.get_by_test_id("login-error-message")
        self.create_account_text = page.get_by_text("Don't have an account?", exact=False)

    def open(self):
        """
        Open login page
        """
        self.page.goto("https://qademo.com/login")

    def login(self, email: str, password: str):
        """
        Login with email and password
        :param email: valid username or email
        :param password: valid password
        :return:
        """
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()
