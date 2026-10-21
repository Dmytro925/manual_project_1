import allure
import pytest
from playwright.sync_api import Page, expect

from src.pages import LoginPage


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
def test_invalid_credentials_rejection(page: Page, username: str, password: str, login_page: LoginPage):
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