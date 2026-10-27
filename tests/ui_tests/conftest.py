import re
from collections.abc import Generator
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from config.environments import get_admin_user, get_locked_user, get_standard_user
from src.pages import CatalogPage, LoginPage

SCREENSHOT_NAME_PATTERN = re.compile(r"^test-failed-\d+\.png$")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(
    item: pytest.Item,
    nextitem: pytest.Item | None,
) -> Generator[None, pytest.TestReport]:
    """Attach failure screenshots to the Allure report."""
    yield

    artifacts_dir = getattr(item, "funcargs", {}).get("output_path")
    if not artifacts_dir:
        return
    artifacts_path = Path(artifacts_dir)
    if not artifacts_path.is_dir():
        return
    for file in artifacts_path.iterdir():
        if file.is_file() and SCREENSHOT_NAME_PATTERN.match(file.name):
            allure.attach.file(
                str(file),
                name=file.name,
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.fixture()
def login_page(page: Page) -> LoginPage:
    """Provide an opened login page."""

    login_page = LoginPage(page)
    login_page.open()
    return login_page


@pytest.fixture()
def standard_user_catalog_page(page: Page, login_page: LoginPage) -> CatalogPage:
    """Log in as a standard user and provide the catalog page."""
    user = get_standard_user()
    login_page.login(email=user.username, password=user.password)
    login_page.navbar.navbar_username.wait_for(state="visible")
    return CatalogPage(page)


@pytest.fixture()
def login_as_admin_user(page: Page, login_page: LoginPage) -> CatalogPage:
    """Log in as the admin user and provide the catalog page."""
    admin_user = get_admin_user()
    login_page.login(email=admin_user.username, password=admin_user.password)
    login_page.navbar.navbar_username.wait_for(state="visible")
    return CatalogPage(page)


@pytest.fixture()
def login_as_locked_user(login_page: LoginPage) -> LoginPage:
    """Attempt a login with the locked user's credentials."""
    locked_user = get_locked_user()
    login_page.login(email=locked_user.username, password=locked_user.password)
    return login_page


@pytest.fixture()
def standard_user_with_product_in_cart(
    standard_user_catalog_page: CatalogPage,
) -> CatalogPage:
    """Add a product to the cart for the standard user."""

    standard_user_catalog_page.add_to_cart("Laptop Backpack")
    return standard_user_catalog_page
