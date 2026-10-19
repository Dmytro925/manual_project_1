import re
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from config.environments import get_standard_user
from src.pages import CatalogPage, LoginPage

SCREENSHOT_NAME_PATTERN = re.compile(r"^test-failed-\d+\.png$")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):  # noqa: ANN001, ANN201
    """Attach failure screenshots to the Allure report."""
    yield

    output_path = item.funcargs.get("output_path")
    if not output_path:
        return

    artifacts_dir = Path(output_path)
    if not artifacts_dir.is_dir():
        return

    for file in artifacts_dir.iterdir():
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

