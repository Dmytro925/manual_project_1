import base64
import json
from typing import Any

import allure
import pytest

from config.environments import get_admin_user, get_locked_user, get_standard_user
from src.api import AuthClient
from tests.api_tests.conftest import DisposableAccount

ACCESS_TOKEN_TTL_SECONDS = 900


def _jwt_claims(token: str) -> dict[str, Any]:
    """Return a JWT's unverified claims."""
    payload = token.split(".")[1]
    return json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))


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
        assert response.status_code == 200
        payload = response.json()
        assert payload["success"] is True
        data = payload["data"]
        assert isinstance(data["user"]["id"], int)
        assert data["user"]["username"] == standard_user.username
        assert data["user"]["userType"] == "standard"
        access_token = data["accessToken"]
        assert isinstance(access_token, str)
        assert len(access_token.split(".")) == 3
        claims = _jwt_claims(access_token)
        assert claims["exp"] - claims["iat"] == ACCESS_TOKEN_TTL_SECONDS
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
        assert response.json() == {
            "success": False,
            "error": {
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid username or password",
            },
        }


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
    "scenario, invalid_fields",
    [
        ("missing-username", ("username",)),
        ("missing-password", ("password",)),
        ("empty-username", ("username",)),
        ("empty-body", ("username", "password")),
    ],
    ids=["missing-username", "missing-password", "empty-username", "empty-body"],
)
@allure.id("LOGIN-005")
@allure.feature("Auth")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Missing or empty required login fields fail validation ({scenario})")
def test_login_with_missing_or_empty_fields_fails_validation(
    auth_client: AuthClient, scenario: str, invalid_fields: tuple[str, ...]
):
    """Missing or empty required login fields are rejected with HTTP 400 and a
    validation error that names every offending field."""
    standard_user = get_standard_user()
    payloads = {
        "missing-username": {"password": standard_user.password},
        "missing-password": {"username": standard_user.username},
        "empty-username": {"username": "", "password": standard_user.password},
        "empty-body": {},
    }

    with allure.step(f"Send POST /api/auth/login with an invalid body ({scenario})"):
        response = auth_client.post(path="/api/auth/login", json=payloads[scenario])
        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False
        assert body["error"]["name"] == "ZodError"
        issues = body["error"]["issues"]
        assert {issue["path"][0] for issue in issues} == set(invalid_fields)
        assert all(issue["message"] for issue in issues)
        assert "data" not in body


@allure.id("LOGIN-006")
@allure.feature("Auth")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Admin logs in with the date-based dynamic password")
def test_admin_login_with_date_based_password(auth_client: AuthClient):
    """The admin_user account authenticates with the dynamic password formed as
    $Admin followed by the current date in DDMMYYYY format.

    The returned token identifies the caller as an admin.
    """
    admin_user = get_admin_user()

    with allure.step("Send POST /api/auth/login with the date-based admin password"):
        response = auth_client.post(
            path="/api/auth/login",
            json={"username": admin_user.username, "password": admin_user.password},
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["success"] is True
        assert payload["data"]["user"]["username"] == admin_user.username
        assert payload["data"]["user"]["userType"] == "admin"
        access_token = payload["data"]["accessToken"]
        assert len(access_token.split(".")) == 3
        claims = _jwt_claims(access_token)
        assert claims["username"] == admin_user.username
        assert claims["userType"] == "admin"
        assert claims["exp"] - claims["iat"] == ACCESS_TOKEN_TTL_SECONDS


@allure.id("LOGIN-007")
@allure.feature("Auth")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Unknown user gets the same error as a wrong password")
def test_login_unknown_user_matches_wrong_password_error(auth_client: AuthClient):
    """Logging in with a username that does not exist returns exactly the same
    error as an existing account with a wrong password, so the response cannot
    be used to enumerate valid usernames."""
    with allure.step("Send POST /api/auth/login with an unknown username"):
        response = auth_client.post(
            path="/api/auth/login",
            json={"username": "no_such_user_xyz_42", "password": "Whatever_42!"},
        )
        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "error": {
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid username or password",
            },
        }


@allure.id("LOGIN-008")
@allure.feature("Auth")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Malformed JSON body is rejected")
def test_login_with_malformed_json_is_rejected(auth_client: AuthClient):
    """A request that declares Content-Type: application/json but sends a
    syntactically broken JSON body fails with HTTP 400 and a controlled error
    message, without leaking internal server details."""
    with allure.step("Send POST /api/auth/login with a truncated JSON body"):
        response = auth_client.post(
            path="/api/auth/login",
            data='{"username": "standard_user", ',
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400
        payload = response.json()
        assert payload["success"] is False
        assert payload["error"]["code"] == "HTTP_ERROR"
        assert payload["error"]["message"] == "Malformed JSON in request body"
        assert set(payload) == {"success", "error"}
        assert set(payload["error"]) == {"code", "message"}
