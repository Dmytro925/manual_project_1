from playwright.sync_api import Page


class Navbar:
    """Page component representing the navigation bar."""

    def __init__(self, page: Page) -> None:
        """Initialize navigation bar elements."""
        self.page = page

        self.navbar_username = page.get_by_test_id("navbar-username")
        self.navbar_admin_link = page.get_by_test_id("navbar-admin-link")
        self.logout_button = page.get_by_test_id("navbar-logout-button")
        self.sign_in_button = page.get_by_test_id("navbar-signin-link")
        self.sign_in_button = page.get_by_label("Sign in")
        self.cart_link = page.get_by_test_id("navbar-cart-link")
        self.cart_badge = page.get_by_test_id("navbar-cart-badge")

    def logout(self) -> None:
        """Log out the current user."""
        self.logout_button.click()
