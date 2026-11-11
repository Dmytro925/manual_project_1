import allure
import pytest

from config.environments import get_standard_user
from src.api import AuthClient


@allure.id("FR-AUTH-002")
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
    "scenario, expected_status_code",
    [
        ("wrong-password", 401),
        ("wrong-user", 401),
        ("both-wrong", 401),
        ("empty-credentials", 400),
    ],
    ids=["wrong-password", "wrong-user", "both-wrong", "empty-credentials"],
)
@allure.id("FR-AUTH-004")
@allure.epic("Authentication API")
@allure.feature("Login Page (/login)")
@allure.story("POST /api/auth/login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Invalid login attempts API ({scenario})")
def test_login_with_invalid_credentials_api(
    auth_client: AuthClient, scenario: str, expected_status_code: int
):
    """Missing or invalid authentication
    Endpoint: POST /api/auth/login"""
    standard_user = get_standard_user()
    credentials = {
        "wrong-password": (standard_user.username, "wrong_password"),
        "wrong-user": ("wrong_user", standard_user.password),
        "both-wrong": ("wrong_user", "wrong_password"),
        "empty-credentials": ("", ""),
    }
    username, password = credentials[scenario]

    with allure.step(f"Verify invalid credentials ({scenario})"):
        response = auth_client.post(
            path="/api/auth/login",
            json={"username": username, "password": password},
        )

        assert response.status_code == expected_status_code
