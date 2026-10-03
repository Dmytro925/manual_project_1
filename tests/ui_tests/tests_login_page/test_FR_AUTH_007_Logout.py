from playwright.sync_api import expect

from pages.catalog_page import CatalogPage
from pages.home_page import HomePage


def test_logout_as_standart_user(page, login_as_standart_user, add_product_to_cart, logout):
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

    home_page = HomePage(page)

    expect(home_page.navbar.sign_in_button).to_be_visible()

    expect(home_page.navbar.cart_badge).to_have_text("1")
