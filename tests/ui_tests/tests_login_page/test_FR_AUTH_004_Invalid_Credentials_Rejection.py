import pytest
from playwright.sync_api import expect

@pytest.mark.parametrize(
    "username, password",
    [
        ("invalid_user", "invalid_password"),
        ("standard_user", "wrong_password"),
        ("admin", "standard123"),
    ],
)

def test_invalid_credentials_rejection(page, username, password, login_page):
    """Description: Invalid credentials are rejected
    Precondition: User is on login page
    Input: Any invalid username/password combination
    Expected Result:
    Login fails
    Error message displayed: "Invalid username or password"
    User remains on login page"""

    login_page = login_page

    login_page.login(username, password)

    expect(login_page.login_error_message).to_have_text(
        "Invalid username or password"
    )

    expect(page).to_have_url("https://qademo.com/login")