import pytest

from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage


@pytest.fixture()
def login_page(page):
    login_page = LoginPage(page)
    login_page.open()
    return login_page

@pytest.fixture()
def catalog_page(page):
    catalog_page = CatalogPage(page)
    catalog_page.open()
    return catalog_page

@pytest.fixture()
def logout(page):
    catalog_page = CatalogPage(page)
    catalog_page.navbar.logout()