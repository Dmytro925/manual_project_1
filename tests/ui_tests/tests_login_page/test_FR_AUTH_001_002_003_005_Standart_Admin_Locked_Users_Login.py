from playwright.sync_api import expect
from manual_project_1.pages.catalog_page import CatalogPage

def test_login_form_display(login_page):
    """Description: Login page displays username and password input fields
    Acceptance Criteria:
    Username field with label "Username"
    Password field with label "Password". Masked input (not covered in this test)
    "Sign In" button
    Test credentials helper section displayed below form
    "Back to Home" link at bottom"""

    login_page = login_page

    # Username field with label "Username"
    expect(login_page.username_field).to_be_visible()
    expect(login_page.username_field).to_have_attribute(
        "placeholder",
        "Enter your username or email"
    )
    expect(login_page.username_field).to_have_attribute(
        "aria-label",
        "Username or email"
    )

    # Password field with label "Password"
    expect(login_page.password_field).to_be_visible()
    expect(login_page.password_field).to_have_attribute(
        "placeholder",
        "Enter your password"
    )
    expect(login_page.password_field).to_have_attribute(
        "aria-label",
        "Password"
    )

    # "Sign In" button
    expect(login_page.login_button).to_be_visible()
    expect(login_page.login_button).to_be_enabled()
    expect(login_page.login_button).to_have_attribute(
        "aria-label",
        "Sign in"
    )

    # "Back to Home" link at bottom
    expect(login_page.back_home_link).to_be_visible()
    expect(login_page.back_home_link).to_have_text("← Back to Home")
    expect(login_page.back_home_link).to_have_attribute("href", "/")

    # Test credentials helper section displayed below form
    expect(login_page.create_account_link).to_be_visible()
    expect(login_page.create_account_link).to_have_text("Create Account")
    expect(login_page.create_account_link).to_have_attribute("href", "/signup")

def test_standard_user_login(page, login_page):
    """Description: Standard user can login successfully
    Precondition: User is on login page
    Input: Username: standard_user, Password: standard123
    Expected Result:
    Login succeeds
    User redirected to /catalog (or previous protected page)
    Username displayed in navbar
    Access token stored in browser"""

    login_page.login("standard_user", "standard123")

# Check that token is not exist before login
    assert not any(
        cookie["name"] == "refresh_token"
        for cookie in page.context.cookies()
    )

    catalog_page = CatalogPage(page)

    # Login succeeds. Username displayed in navbar. User redirected to /catalog (or previous protected page)
    expect(page).to_have_url("/catalog")
    expect(catalog_page.navbar.navbar_username).to_have_text("standard_user")

    # Access token stored in browser
    assert any(
        cookie["name"] == "refresh_token"
        for cookie in page.context.cookies()
    )

def test_admin_user_login(page, login_as_admin_user):
    """Description: Admin user can login and access admin features
    Precondition: User is on login page
    Input: Username: admin_user, Password: $Admin<ddmmyyyy> (calculated based on current date DDMMYYYY)
    Expected Result:
    Login succeeds
    User redirected to catalog
    "Admin" button visible in navbar
    User can access /admin page"""
    # Check that token is not exist before login
    assert not any(
        cookie["name"] == "refresh_token"
        for cookie in page.context.cookies()
    )

    # Login succeeds. User redirected to catalog
    expect(page).to_have_url("/catalog")

    catalog_page = CatalogPage(page)

    expect(catalog_page.navbar.navbar_username).to_have_text("admin_user")

    # "Admin" button visible in navbar
    expect(catalog_page.navbar.navbar_admin_link).to_have_text("Admin")

    # Access token stored in browser
    assert any(
        cookie["name"] == "refresh_token"
        for cookie in page.context.cookies()
    )

def test_locked_user_login(page, login_page, login_as_locked_user):
    """Description: Locked user cannot login
    Precondition: User is on login page
    Input: Username: locked_user, Password: locked123
    Expected Result:
    Login fails
    Error message displayed: "Account is locked"
    User remains on login page"""

    # User remains on login page
    expect(page).to_have_url("/login")

    # Access token is not stored in browser
    assert not any(
        cookie["name"] == "refresh_token"
        for cookie in page.context.cookies()
    )

    # Error message displayed: "Account is locked"
    expect(login_page.login_error_message).to_have_text("Account is locked")