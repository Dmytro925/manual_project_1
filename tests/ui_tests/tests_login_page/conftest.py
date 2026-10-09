import pytest

from src.pages.login_page import LoginPage
from test_data.users import LOCKED_USER
from test_data.users import get_admin_user

@pytest.fixture()
def login_as_admin_user(page, login_page):
    admin_user = get_admin_user()
    login_page.login(
        email=admin_user["username"],
        password=admin_user["password"]
    )

@pytest.fixture()
def login_as_locked_user(page):
    login_as_locked_user = LoginPage(page)
    login_as_locked_user.open()
    login_as_locked_user.login(
        email=LOCKED_USER["username"],
        password=LOCKED_USER["password"]
    )
    return login_as_locked_user

@pytest.fixture()
def standard_user_with_product_in_cart(standard_user_catalog_page):
    standard_user_catalog_page.add_to_cart_button.click()
    return standard_user_catalog_page