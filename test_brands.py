import pytest
import re
from playwright.sync_api import Page, sync_playwright, expect
from config import brands


# Fixture to start a browser session for each test
@pytest.fixture(scope="function", params=["chromium", "webkit"])
def page_fixture(request):
    with sync_playwright() as p:
        browser = getattr(p, request.param).launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()


@pytest.mark.parametrize("brand, data", brands.items())
def test_homepage_loads(page_fixture: Page, brand, data):
    """Check if the homepage loads properly for each brand."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")
    print(f"{brand} - Page Title: {page_fixture.title()}")


@pytest.mark.parametrize("brand, data", brands.items())
def test_get_app_button(page_fixture: Page, brand, data):
    """Verify if the 'Get App' button exists based on the brand's feature."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")


    get_app_button = page_fixture.locator("xpath=/html/body/main/div/nav/div[3]/button[2]")

    if data["features"].get("get_app"):
        expect(get_app_button).to_be_visible()
        print(f"✅ 'Get App' button is present on {brand}")
    else:
        expect(get_app_button).not_to_be_visible()
        print(f"'Get App' button should NOT be present on {brand} (Test should fail if found)")


@pytest.mark.parametrize("brand, data", brands.items())
def test_become_creator_option(page_fixture: Page, brand, data):
    """Verify if the 'Become a Creator' option exists in the sidebar."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")

    become_creator_option = page_fixture.locator("xpath=//a[contains(text(), 'Become a Creator')]")

    if data["features"].get("become_creator"):
        expect(become_creator_option).to_be_visible()
        print(f" 'Become a Creator' option is present on {brand}")
    else:
        expect(become_creator_option).not_to_be_visible()
        print(f"'Become a Creator' option should NOT be present on {brand} (Test should fail if found)")


@pytest.mark.parametrize("brand, data", brands.items())
def test_login_button(page_fixture: Page, brand, data):
    """Verify if the login button exists for gopuff_old and doesn't exist for others."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")

    login_button = page_fixture.locator("xpath=/html/body/main/div/nav/div[2]/button[2]/p")

    if data["features"].get("login"):
        expect(login_button).to_be_visible()
        print(f"Login button is visible on {brand}")
        login_button.click()
        page_fixture.wait_for_timeout(1000)
    else:
        expect(login_button).not_to_be_visible()
        print(f"Login button should NOT be present on {brand} (Test should fail if found)")


@pytest.mark.parametrize("brand, data", brands.items())
def test_login_functionality(page_fixture: Page, brand, data):
    """Test the login process for gopuff_old only."""
    if data["features"].get("login"):
        page_fixture.goto(data["url"], wait_until="domcontentloaded")
        page_fixture.wait_for_timeout(1000)

        # Find and click the login button
        login_button = page_fixture.locator("xpath=/html/body/main/div/nav/div[2]/button[2]/p")
        expect(login_button).to_be_visible()
        login_button.click()
        page_fixture.wait_for_timeout(1000)

        # Find the email input field and enter the email
        email_field = page_fixture.locator("xpath=//input[contains(@id, 'form-item')]")
        expect(email_field).to_be_visible()
        email_field.fill("testuser@yopmail.com")

        # Press Enter to submit the login form
        email_field.press("Enter")
        page_fixture.wait_for_timeout(2000)

        print("Login form filled and submitted successfully.")
    else:
        pytest.skip(f"Skipping login test for {brand} (Login feature not available)")
