from playwright.sync_api import expect

from pages.catalog_page import CatalogPage


def test_logout_as_standart_user(page, login_as_standart_user, logout):
    """FR-AUTH-007: Logout Functionality
Description: Logged-in user can logout
Precondition: User is authenticated
Action: Click logout button (icon) in navbar
Expected Result:
User session cleared
User redirected to home page
"Sign In" button appears in navbar
Cart state persisted (if applicable)"""

    expect(page).to_have_url("https://qademo.com/")

    # Access token is not stored in browser
    assert not any(
        cookie["name"] == "refresh_token"
        for cookie in page.context.cookies()
    )

    expect(page.get_by_label("Sign in")).to_be_visible()
