from playwright.sync_api import expect
from manual_project_1.pages.home_page import HomePage
from manual_project_1.pages.login_page import LoginPage


def test_standard_user_logout(page, standard_user_with_product_in_cart):
    """FR-AUTH-007: Logout Functionality
Description: Logged-in user can logout
Precondition: User is authenticated
Action: Click logout button (icon) in navbar
Expected Result:
User session cleared
User redirected to home page
"Sign In" button appears in navbar
Cart state persisted (if applicable)"""

    catalog_page = standard_user_with_product_in_cart
    catalog_page.navbar.logout_button.click()

    expect(page).to_have_url("/")

    home_page = HomePage(page)
    expect(home_page.navbar.sign_in_button).to_be_visible()
    expect(home_page.navbar.cart_badge).to_have_text("1")

def test_standard_user_session_persistence(page, standard_user_catalog_page):
    """FR-AUTH-008: Session Persistence
    Description: User session persists across page refresh
    Precondition: User is authenticated
    Action: Refresh the browser page
    Expected Result:
    User remains logged in
    Username still displayed in navbar"""

    page.reload()

    expect(page).to_have_url("/catalog")
    expect(standard_user_catalog_page.navbar.navbar_username).to_be_visible()
    expect(standard_user_catalog_page.navbar.navbar_username).to_have_text("standard_user")

def test_standard_user_protected_route_redirect(page, login_page):
    """FR-AUTH-009: Protected Route Redirect
    Description: Unauthenticated users redirected to login for protected routes
    Precondition: User is not logged in
    Action: Navigate directly to /checkout or /orders
    Expected Result:
    User redirected to /login
    After login, user redirected to originally requested page"""

    page.goto("/checkout")

    expect(page).to_have_url("/login")

    page.goto("/orders")

    expect(page).to_have_url("/login")


