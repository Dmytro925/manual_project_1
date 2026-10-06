import pytest
from test_data.users import STANDARD_USER
from manual_project_1.pages.login_page import LoginPage
from manual_project_1.pages.catalog_page import CatalogPage


@pytest.fixture()
def login_page(page):
    login_page = LoginPage(page)
    login_page.open()
    return login_page

@pytest.fixture()
def login_as_standard_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(
        email=STANDARD_USER["username"],
        password=STANDARD_USER["password"]
    )
    login_page.navbar.navbar_username.wait_for(state="visible")

@pytest.fixture()
def standard_user_catalog_page(page, login_as_standard_user):
    catalog_page = CatalogPage(page)
    #catalog_page.open()
    return catalog_page

