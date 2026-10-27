from playwright.sync_api import Page

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.username_field = page.get_by_test_id("username-input")
        self.password_field = page.get_by_test_id("password-input")
        self.login_button = page.get_by_test_id("login-submit-button")
        self.back_home_link = page.get_by_test_id("back-to-home-link")
        self.create_account_link = page.get_by_test_id("sign-up-link")
        self.login_error_message = page.get_by_test_id("login-error-message")
        self.create_account_text = page.get_by_text(
            "Don't have an account?", exact=False
        )

    def open(self) -> None:
        """Open the login page."""

        self.page.goto("/login")

    def login(self, email: str, password: str) -> None:
        """Log in with email and password.

        :param email: Valid username or email.
        :param password: Valid password.
        """

        self.username_field.fill(email)
        self.password_field.fill(password)
        self.login_button.click()
