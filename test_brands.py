import pytest
from playwright.sync_api import Page, sync_playwright, expect
from config import brands


# Fixture to start a browser session for each test
@pytest.fixture(scope="function", params=["chromium"])
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
    print(f"✅ {brand} - Page Title: {page_fixture.title()}")


@pytest.mark.parametrize("brand, data", brands.items())
def test_get_app_button(page_fixture: Page, brand, data):
    """Verify if the 'Get App' button exists where expected."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")

    # ✅ Locator for "Get App" button
    get_app_button = page_fixture.locator("//button[contains(text(), 'Get App')]")

    if data["features"].get("get_app"):
        expect(get_app_button).to_be_visible()
        print(f"✅ 'Get App' button is present on {brand}")
    else:
        assert not get_app_button.is_visible(), f"❌ 'Get App' button should NOT be present on {brand} (Test should fail if found)"
        print(f"✅ 'Get App' button is correctly NOT visible on {brand}")


@pytest.mark.parametrize("brand, data", brands.items())
def test_become_creator_option(page_fixture: Page, brand, data):
    """Verify if the 'Become a Creator' option exists where expected."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")

    # ✅ Locator for "Become a Creator" option
    become_creator_option = page_fixture.locator("//a[contains(text(), 'Become a Creator')]")

    if data["features"].get("become_creator"):
        expect(become_creator_option).to_be_visible()
        print(f"✅ 'Become a Creator' option is present on {brand}")
    else:
        assert not become_creator_option.is_visible(), f"❌ 'Become a Creator' option should NOT be present on {brand} (Test should fail if found)"
        print(f"✅ 'Become a Creator' option is correctly NOT visible on {brand}")


@pytest.mark.parametrize("brand, data", brands.items())
def test_login_button(page_fixture: Page, brand, data):
    """Verify if the login button exists for gopuff_old and not for others."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")

    # ✅ Locator for "Login" button
    login_button = page_fixture.locator("//button[contains(text(), 'Log in')]")

    if data["features"].get("login"):
        expect(login_button).to_be_visible()
        print(f"✅ Login button is visible on {brand}")
    else:
        assert not login_button.is_visible(), f"❌ Login button should NOT be present on {brand} (Test should fail if found)"
        print(f"✅ Login button is correctly NOT visible on {brand}")


@pytest.mark.parametrize("brand, data", brands.items())
def test_login_functionality(page_fixture: Page, brand, data):
    """Perform login only for gopuff_old, otherwise skip."""

    page_fixture.goto(data["url"], wait_until="domcontentloaded")

    # ✅ Locator for "Login" button
    login_button = page_fixture.locator("//button[contains(text(), 'Log in')]")

    # ✅ Only run login test for gopuff_old
    if brand != "gopuff_old":
        pytest.skip(f"⏭ Skipping login test for {brand} (Login feature not supported)")

    # ✅ Ensure login button is found for gopuff_old
    try:
        page_fixture.wait_for_selector("//button[contains(text(), 'Log in')]", timeout=5000)
    except Exception:
        pytest.fail(f"❌ Login button NOT found on {brand}, but it should be present!")

    # ✅ Perform login process
    expect(login_button).to_be_visible()
    print(f"✅ Login button found on {brand}, proceeding with login...")
    login_button.click()
    page_fixture.wait_for_timeout(2000)

    # ✅ Find and enter email
    email_field = page_fixture.locator("//input[@type='email']")
    expect(email_field).to_be_visible()
    email_field.fill("testuser@yopmail.com")

    # ✅ Submit login form
    email_field.press("Enter")
    page_fixture.wait_for_timeout(2000)

    print("✅ Login form filled and submitted successfully.")
