import pytest
from playwright.sync_api import Page

from config.environments import get_standard_user
from src.pages import CatalogPage, LoginPage


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
    user = get_standard_user()
    login_page.login(
        email=user.username,
        password=user.password,
    )
    login_page.navbar.navbar_username.wait_for(state="visible")
    return CatalogPage(page)

