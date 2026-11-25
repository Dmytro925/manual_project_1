import base64
import json

import allure
import pytest

from config.environments import get_locked_user, get_standard_user
from src.api import AuthClient
from tests.api_tests.accounts import DisposableAccount

ACCESS_TOKEN_TTL_SECONDS = 900


def _jwt_lifetime_seconds(token: str) -> int:
    """Return a JWT's lifetime in seconds from its unverified claims."""
    payload = token.split(".")[1]
    claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    return int(claims["exp"]) - int(claims["iat"])


@allure.id("LOGIN-001")
@allure.feature("Auth")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Successful login with valid standard user credentials")
@allure.issue(
    "https://github.com/Dmytro925/manual_project_1/issues/50",
    "BUG #50: login response omits refreshToken in the body",
)
def test_standard_user_login_succeeds(auth_client: AuthClient):
    """The pre-seeded standard customer account authenticates with its correct
    username and password.

    The API returns the success flag, the user identity, a usable JWT access
    token that expires in 15 minutes, and a refresh token.
    """
    standard_user = get_standard_user()

    with allure.step("Send POST /api/auth/login with the standard user credentials"):
        response = auth_client.post(
            path="/api/auth/login",
            json={
                "username": standard_user.username,
                "password": standard_user.password,
            },
        )

    with allure.step("Verify the success flag and the returned user identity"):
        assert response.status_code == 200
        payload = response.json()
        assert payload["success"] is True
        data = payload["data"]
        assert isinstance(data["user"]["id"], int)
        assert data["user"]["username"] == standard_user.username
        assert data["user"]["userType"] == "standard"

    with allure.step("Verify the access token is a JWT that expires in 15 minutes"):
        access_token = data["accessToken"]
        assert isinstance(access_token, str)
        assert len(access_token.split(".")) == 3
        assert _jwt_lifetime_seconds(access_token) == ACCESS_TOKEN_TTL_SECONDS

    with allure.step("Verify a refresh token is returned"):
        refresh_token = data.get("refreshToken")
        assert isinstance(refresh_token, str)
        assert refresh_token


@allure.id("LOGIN-002")
@allure.feature("Auth")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Login accepts the account email as username, ignoring letter case")
def test_login_accepts_account_email_ignoring_case(
    auth_client: AuthClient, disposable_account: DisposableAccount
):
    """The username field of the login request accepts the email address
    registered on the account instead of the username, and the lookup is not
    case-sensitive."""
    with allure.step("Send POST /api/auth/login with the account email"):
        response = auth_client.post(
            path="/api/auth/login",
            json={
                "username": disposable_account.email,
                "password": disposable_account.password,
            },
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["success"] is True
        user = payload["data"]["user"]
        assert user["username"] == disposable_account.username
        assert user["userType"] == "standard"
        access_token = payload["data"]["accessToken"]
        assert isinstance(access_token, str)
        assert access_token
        assert len(access_token.split(".")) == 3

    with allure.step("Send POST /api/auth/login with the email in upper case"):
        response = auth_client.post(
            path="/api/auth/login",
            json={
                "username": disposable_account.email.upper(),
                "password": disposable_account.password,
            },
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["success"] is True
        assert payload["data"]["user"]["username"] == disposable_account.username


@allure.id("LOGIN-003")
@allure.feature("Auth")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Login with a wrong password is rejected")
def test_login_with_wrong_password_is_rejected(auth_client: AuthClient):
    """An existing account combined with an incorrect password is refused with
    the invalid-credentials error and HTTP 401.

    The response contains no token and does not reveal whether the username or
    the password was wrong.
    """
    standard_user = get_standard_user()

    with allure.step(
        "Send POST /api/auth/login with the standard user's username and a wrong password"
    ):
        response = auth_client.post(
            path="/api/auth/login",
            json={
                "username": standard_user.username,
                "password": "WrongPass_42!",
            },
        )
        assert response.status_code == 401
        payload = response.json()
        assert payload["success"] is False
        assert payload["error"]["code"] == "INVALID_CREDENTIALS"
        assert payload["error"]["message"] == "Invalid username or password"
        assert "data" not in payload


@allure.id("LOGIN-004")
@allure.feature("Auth")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Login of the locked account is rejected")
def test_login_of_locked_account_is_rejected(auth_client: AuthClient):
    """The pre-seeded locked account cannot authenticate even with its correct
    password: the API refuses with HTTP 403 and a locked-account error, and
    returns no token."""
    locked_user = get_locked_user()

    with allure.step("Send POST /api/auth/login with the locked account credentials"):
        response = auth_client.post(
            path="/api/auth/login",
            json={
                "username": locked_user.username,
                "password": locked_user.password,
            },
        )
        assert response.status_code == 403
        payload = response.json()
        assert payload["success"] is False
        assert payload["error"]["code"] == "ACCOUNT_LOCKED"
        assert payload["error"]["message"] == "Account is locked"
        assert "data" not in payload


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
