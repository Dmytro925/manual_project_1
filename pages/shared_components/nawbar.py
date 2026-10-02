from playwright.sync_api import Page


class Navbar:

    def __init__(self, page: Page):
        self.page = page

        self.navbar_username = page.get_by_test_id("navbar-username")
        self.navbar_admin_link = page.get_by_test_id("navbar-admin-link")
        self.logout_button = page.get_by_test_id("navbar-logout-button")
        self.sign_in_button = page.get_by_test_id("navbar-signin-link")
        self.sign_in_button = page.get_by_label("Sign in")

    def logout(self):
        self.logout_button.click()