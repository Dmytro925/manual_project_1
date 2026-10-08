import pytest
import requests
from test_data.users import STANDARD_USER
import logging

@pytest.fixture(autouse=True)
def log_api_response(monkeypatch):
    logger = logging.getLogger(__name__)
    original_request = requests.Session.request

    def request(self, *args, **kwargs):
        response = original_request(self, *args, **kwargs)

        logger.info("Response body:\n%s", response.text)

        return response

    monkeypatch.setattr(requests.Session, "request", request)

@pytest.fixture()
def standard_user_login_api():
    response = requests.post(
        "https://qademo.com/api/auth/login",
        json={
            "username": STANDARD_USER["username"],
            "password": STANDARD_USER["password"],
        },
    )

    return response