import pytest
from playwright.sync_api import Page

from src.pages import CatalogPage, LoginPage
from test_data.users import LOCKED_USER, get_admin_user


@pytest.fixture()
def login_as_admin_user(login_page: LoginPage) -> None:
    """Log in as an admin user."""

    admin_user = get_admin_user()
    login_page.login(
        email=admin_user["username"],
        password=admin_user["password"]
    )

@pytest.fixture()
def login_as_locked_user(page: Page) -> LoginPage:
    """Open the login page for a locked user."""

    login_as_locked_user = LoginPage(page)
    login_as_locked_user.open()
    login_as_locked_user.login(
        email=LOCKED_USER["username"],
        password=LOCKED_USER["password"]
    )
    return login_as_locked_user

@pytest.fixture()
def standard_user_with_product_in_cart(
    standard_user_catalog_page: CatalogPage,
) -> CatalogPage:
    """Add a product to the cart for the standard user."""

    standard_user_catalog_page.add_to_cart_button.click()
    return standard_user_catalog_page