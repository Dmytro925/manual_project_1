import pytest
from playwright.sync_api import Page

from src.pages import CatalogPage, LoginPage
from test_data.users import STANDARD_USER


@pytest.fixture()
def login_page(page: Page) -> LoginPage:
    """Provide an opened login page."""

    login_page = LoginPage(page)
    login_page.open()
    return login_page

@pytest.fixture()
def standard_user_catalog_page(page: Page) -> CatalogPage:
    """Log in as a standard user and provide the catalog page."""

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(
        email=STANDARD_USER["username"],
        password=STANDARD_USER["password"]
    )
    login_page.navbar.navbar_username.wait_for(state="visible")
    return CatalogPage(page)

