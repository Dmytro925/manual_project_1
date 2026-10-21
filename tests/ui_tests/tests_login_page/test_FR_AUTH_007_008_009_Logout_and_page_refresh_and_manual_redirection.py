import allure
from playwright.sync_api import Page, expect

from src.pages import CatalogPage, HomePage, LoginPage


@allure.id("FR_AUTH_007")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Logout Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Logged-in user can logout")
def test_standard_user_logout(page: Page, standard_user_with_product_in_cart: CatalogPage):
    """Description: Logged-in user can logout
    Precondition: User is authenticated
    Action: Click logout button (icon) in navbar
    Expected Result:
    User session cleared
    User redirected to home page
    "Sign In" button appears in navbar
    Cart state persisted (if applicable)"""

    with allure.step("Verify that / page is shown if user logged out with product"):
        catalog_page = standard_user_with_product_in_cart
        catalog_page.navbar.logout_button.click()
        expect(page).to_have_url("/")

    with allure.step("Verify that cart_badge is NOT empty after logout"):
        home_page = HomePage(page)
        expect(home_page.navbar.sign_in_button).to_be_visible()
        expect(home_page.navbar.cart_badge).to_have_text("1")

@allure.id("FR_AUTH_008")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Session Persistence")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("User session persists across page refresh")
def test_standard_user_session_persistence(page: Page, standard_user_catalog_page: CatalogPage):
    """Description: User session persists across page refresh
    Precondition: User is authenticated
    Action: Refresh the browser page
    Expected Result:
    User remains logged in
    Username still displayed in navbar"""

    with allure.step("Verify that /catalog after page reload"):
        page.reload()
        expect(page).to_have_url("/catalog")

    with allure.step("Verify that standard_user is shown in navbar after page reload"):
        expect(standard_user_catalog_page.navbar.navbar_username).to_be_visible()
        expect(standard_user_catalog_page.navbar.navbar_username).to_have_text("standard_user")

@allure.id("FR_AUTH_009")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Protected Route Redirect")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Unauthenticated users redirected to login for protected routes")
def test_standard_user_protected_route_redirect(page: Page, login_page: LoginPage):
    """Description: Unauthenticated users redirected to login for protected routes
    Precondition: User is not logged in
    Action: Navigate directly to /checkout or /orders
    Expected Result:
    User redirected to /login
    After login, user redirected to originally requested page"""

    with allure.step("Verify that /login is shown after /checkout navigation"):
        page.goto("/checkout")
        expect(page).to_have_url("/login")

    with allure.step("Verify that /login is shown after /orders navigation"):
        page.goto("/orders")
        expect(page).to_have_url("/login")


