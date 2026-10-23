import allure
import pytest

from config.environments import get_standard_user
from src.api import AuthClient


@allure.id("FR_AUTH_002")
@allure.epic("Authentication API")
@allure.feature("Login Page (/login)")
@allure.story("POST /api/auth/login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Standard user login API")
def test_standard_user_login_api(auth_client: AuthClient):
    """Getting an Access Token
    Endpoint: POST /api/auth/login
    Access Token: Expires in 15 minutes
    Refresh Token: Expires in 7 days"""
    expected_status_code = 200

    with allure.step("Verify that standard_user is logged in"):
        standard_user = get_standard_user()
        response = auth_client.post(
            path="/api/auth/login",
            json={
                "username": standard_user.username,
                "password": standard_user.password,
            },
        )

        assert response.status_code == expected_status_code
        decoded_content = response.json()
        assert decoded_content["data"]["user"]["username"] == standard_user.username
        assert decoded_content["data"]["accessToken"]


@pytest.mark.parametrize(
    "username, password, expected_status_code",
    [
        ("standard_user", "wrong_password", 401),
        ("wrong_user", "standard123", 401),
        ("wrong_user", "wrong_password", 401),
        ("", "", 400),
    ],
)
@allure.id("FR_AUTH_002")
@allure.epic("Authentication API")
@allure.feature("Login Page (/login)")
@allure.story("POST /api/auth/login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Standard user login API")
def test_login_with_invalid_credentials_api(
    auth_client: AuthClient, username: str, password: str, expected_status_code: str
):
    """Missing or invalid authentication
    Endpoint: POST /api/auth/login"""

    with allure.step("Verify invalid credentials for standard_user"):
        response = auth_client.post(
            path="/api/auth/login",
            json={"username": username, "password": password},
        )

        assert response.status_code == expected_status_code
