import allure
import pytest
from playwright.sync_api import Page, expect

from src.pages import CatalogPage, HomePage, LoginPage


@allure.id("FR_AUTH_001")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Login form display")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Login page displays username and password input fields")
def test_login_form_display(login_page: LoginPage):
    """Description: Login page displays username and password input fields
    Acceptance Criteria:
    Username field with label "Username"
    Password field with label "Password". Masked input (not covered in this test)
    "Sign In" button
    Test credentials helper section displayed below form
    "Back to Home" link at bottom"""

    with allure.step("Verify username field"):
        expect(login_page.username_field).to_be_visible()
        expect(login_page.username_field).to_be_enabled()
        expect(login_page.username_field).to_have_attribute(
            "aria-label", "Username or email"
        )

    with allure.step("Verify password field"):
        expect(login_page.password_field).to_be_visible()
        expect(login_page.password_field).to_be_enabled()
        expect(login_page.password_field).to_have_attribute("aria-label", "Password")

    with allure.step("Verify sign-in button"):
        expect(login_page.login_button).to_be_visible()
        expect(login_page.login_button).to_be_enabled()
        expect(login_page.login_button).to_have_attribute("aria-label", "Sign in")

    with allure.step("Verify navigation and helper links"):
        expect(login_page.back_home_link).to_be_visible()
        expect(login_page.back_home_link).to_have_text("← Back to Home")
        expect(login_page.back_home_link).to_have_attribute("href", "/")

        expect(login_page.create_account_link).to_be_visible()
        expect(login_page.create_account_link).to_have_text("Create Account")
        expect(login_page.create_account_link).to_have_attribute("href", "/signup")


@allure.id("FR_AUTH_002")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Standard User Login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Standard user can login successfully")
def test_standard_user_login(page: Page, standard_user_catalog_page: CatalogPage):
    """Description: Standard user can login successfully
    Precondition: User is on login page
    Input: Username: standard_user, Password: standard123
    Expected Result:
    Login succeeds
    User redirected to /catalog (or previous protected page)
    Username displayed in navbar
    Access token stored in browser"""

    with allure.step("Verify user navigation to catalog page after log in"):
        expect(page).to_have_url("/catalog")

    with allure.step("Verify that standard_user is shown in navbar"):
        expect(standard_user_catalog_page.navbar.navbar_username).to_have_text(
            "standard_user"
        )

    with allure.step("Verify that refresh token is stored in browser"):
        assert any(
            cookie["name"] == "refresh_token" for cookie in page.context.cookies()
        )


@allure.id("FR_AUTH_005")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Admin User Login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Admin user can login and access admin features")
def test_admin_user_login(page: Page, login_as_admin_user: LoginPage):
    """Description: Admin user can login and access admin features
    Precondition: User is on login page
    Input: Username: admin_user, Password: $Admin<ddmmyyyy> (calculated based on current date DDMMYYYY)
    Expected Result:
    Login succeeds
    User redirected to catalog
    "Admin" button visible in navbar
    User can access /admin page"""

    with allure.step("Verify that refresh token is NOT stored in browser"):
        assert not any(
            cookie["name"] == "refresh_token" for cookie in page.context.cookies()
        )

    with allure.step("Verify user navigation to catalog page after log in"):
        expect(page).to_have_url("/catalog")
        catalog_page = CatalogPage(page)

    with allure.step("Verify that admin_user is shown in navbar"):
        expect(catalog_page.navbar.navbar_username).to_have_text("admin_user")
        expect(catalog_page.navbar.navbar_admin_link).to_have_text("Admin")

    with allure.step("Verify that refresh token is stored in browser"):
        assert any(
            cookie["name"] == "refresh_token" for cookie in page.context.cookies()
        )


@allure.id("FR_AUTH_003")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Locked User Login Rejection")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Locked user cannot login")
def test_locked_user_cannot_login(
    page: Page, login_page: LoginPage, login_as_locked_user: LoginPage
):
    """Description: Locked user cannot login
    Precondition: User is on login page
    Input: Username: locked_user, Password: locked123
    Expected Result:
    Login fails
    Error message displayed: "Account is locked"
    User remains on login page"""

    with allure.step("Verify that user is on login page"):
        expect(page).to_have_url("/login")

    with allure.step("Verify that refresh token is NOT stored in browser"):
        assert not any(
            cookie["name"] == "refresh_token" for cookie in page.context.cookies()
        )

    with allure.step("Verify that account is locked"):
        expect(login_page.login_error_message).to_have_text("Account is locked")


@pytest.mark.parametrize(
    "username, password",
    [
        ("invalid_user", "invalid_password"),
        ("standard_user", "wrong_password"),
        ("admin", "standard123"),
    ],
)
@allure.id("FR_AUTH_003")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Invalid Credentials Rejection")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Invalid credentials are rejected (as {username})")
def test_invalid_credentials_rejection(
    page: Page, username: str, password: str, login_page: LoginPage
):
    """Description: Invalid credentials are rejected
    Precondition: User is on login page
    Input: Any invalid username/password combination
    Expected Result:
    Login fails
    Error message displayed: "Invalid username or password"
    User remains on login page"""

    with allure.step("Verify that 'Invalid username or password' message is displayed"):
        login_page.login(username, password)
        expect(login_page.login_error_message).to_have_text(
            "Invalid username or password"
        )

    with allure.step("Verify that Login page is shown"):
        expect(page).to_have_url("/login")


@allure.id("FR_AUTH_007")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Logout Functionality")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Logged-in user can logout")
def test_standard_user_logout(
    page: Page, standard_user_with_product_in_cart: CatalogPage
):
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
        expect(home_page.navbar.sign_in_link).to_be_visible()
        expect(home_page.navbar.cart_badge).to_have_text("1")


@allure.id("FR_AUTH_008")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Session Persistence")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("User session persists across page refresh")
def test_standard_user_session_persistence(
    page: Page, standard_user_catalog_page: CatalogPage
):
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
        expect(standard_user_catalog_page.navbar.navbar_username).to_have_text(
            "standard_user"
        )


@allure.id("FR_AUTH_009")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Protected Route Redirect")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Unauthenticated users redirected to login for protected routes")
def test_unauthenticated_user_redirected_to_login(page: Page, login_page: LoginPage):
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
