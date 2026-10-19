import allure
from playwright.sync_api import Page, expect

from src.pages import CatalogPage, LoginPage


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
        expect(login_page.username_field).to_have_attribute(
            "placeholder",
            "Enter your username or email"
        )
        expect(login_page.username_field).to_have_attribute(
            "aria-label",
            "Username or email"
        )

    with allure.step("Verify password field"):
        expect(login_page.password_field).to_be_visible()
        expect(login_page.password_field).to_have_attribute(
            "placeholder",
            "Enter your password"
        )
        expect(login_page.password_field).to_have_attribute(
            "aria-label",
            "Password"
        )

    with allure.step("Verify sign-in button"):
        expect(login_page.login_button).to_be_visible()
        expect(login_page.login_button).to_be_enabled()
        expect(login_page.login_button).to_have_attribute(
            "aria-label",
            "Sign in"
        )

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
        expect(standard_user_catalog_page.navbar.navbar_username).to_have_text("standard_user")

    with allure.step("Verify that refresh token is stored in browser"):
        assert any(
            cookie["name"] == "refresh_token"
            for cookie in page.context.cookies()
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
    assert not any(
        cookie["name"] == "refresh_token"
        for cookie in page.context.cookies()
    )

    with allure.step("Verify user navigation to catalog page after log in"):
        expect(page).to_have_url("/catalog")

        catalog_page = CatalogPage(page)

    with allure.step("Verify that admin_user is shown in navbar"):
        expect(catalog_page.navbar.navbar_username).to_have_text("admin_user")

        expect(catalog_page.navbar.navbar_admin_link).to_have_text("Admin")

    with allure.step("Verify that refresh token is stored in browser"):
        assert any(
            cookie["name"] == "refresh_token"
            for cookie in page.context.cookies()
        )

@allure.id("FR_AUTH_003")
@allure.epic("Authentication Module")
@allure.feature("Login Page (/login)")
@allure.story("Locked User Login Rejection")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Locked user cannot login")
def test_locked_user_login(page: Page, login_page: LoginPage, login_as_locked_user: LoginPage):
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
            cookie["name"] == "refresh_token"
            for cookie in page.context.cookies()
        )

    with allure.step("Verify that account is locked"):
        expect(login_page.login_error_message).to_have_text("Account is locked")