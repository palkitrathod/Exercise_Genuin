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

    get_app_button = page_fixture.locator("//button[contains(text(), 'Get App')]")

    if data["features"]["get_app"]:
        expect(get_app_button).to_be_visible()
        print(f"✅ 'Get App' button is present on {brand}")
    else:
        assert not get_app_button.is_visible(), f"❌ 'Get App' button should NOT be present on {brand} (Test Failed!)"
        print(f"✅ 'Get App' button is correctly NOT visible on {brand}")


@pytest.mark.parametrize("brand, data", brands.items())
def test_become_creator_option(page_fixture: Page, brand, data):
    """Verify if the 'Become a Creator' option exists where expected."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")

    become_creator_option = page_fixture.locator(
        "(//p[@class='w-64 overflow-hidden p-3 text-start text-body-1-bold'])[1]")

    if data["features"]["become_creator"]:
        expect(become_creator_option).to_be_visible()
        print(f"✅ 'Become a Creator' option is present on {brand}")
    else:
        assert not become_creator_option.is_visible(), f"❌ 'Become a Creator' option should NOT be present on {brand} (Test Failed!)"
        print(f"✅ 'Become a Creator' option is correctly NOT visible on {brand}")


@pytest.mark.parametrize("brand, data", brands.items())
def test_login_button(page_fixture: Page, brand, data):
    """Verify if the login button exists for gopuff_old and not for others."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")

    login_button = page_fixture.locator(
        "(//button[@class='inline-flex items-center justify-center rounded-md transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary-600 after::bg-primary-600 py-2 h-8 gap-2 px-4'])[1]")

    if data["features"]["login"]:
        expect(login_button).to_be_visible()
        print(f"✅ Login button is present on {brand}")
    else:
        assert not login_button.is_visible(), f"❌ Login button should NOT be present on {brand} (Test Failed!)"
        print(f"✅ Login button is correctly NOT visible on {brand}")


@pytest.mark.parametrize("brand, data", brands.items())
def test_login_functionality(page_fixture: Page, brand, data):
    """Perform login only for gopuff_old, otherwise skip."""

    page_fixture.goto(data["url"], wait_until="domcontentloaded")

    if not data["features"]["login"]:
        pytest.skip(f"⏭ Skipping login test for {brand} (Login feature not supported)")

    # Find and click the login button
    login_button = page_fixture.locator(
        "(//button[@class='inline-flex items-center justify-center rounded-md transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary-600 after::bg-primary-600 py-2 h-8 gap-2 px-4'])[1]")

    try:
        expect(login_button).to_be_visible()
        login_button.click()
        page_fixture.wait_for_timeout(2000)
    except:
        pytest.fail(f"❌ ERROR: Login button NOT found on {brand}")

    # Find and enter email in the login form
    email_field = page_fixture.locator("//input[@type='email']")

    try:
        expect(email_field).to_be_visible()
        email_field.fill("testuser@yopmail.com")
        email_field.press("Enter")
        print(f"✅ Login form filled and submitted successfully for {brand}")
    except:
        pytest.fail(f"❌ ERROR: Could not find login email field on {brand}")
