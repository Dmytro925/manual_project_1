from playwright.sync_api import Page, expect


def test_home_page(page: Page):
    page.goto("https://qademo.com/")

    expect(page).to_have_title("QA Demo - Your Playground for Automated Testing")