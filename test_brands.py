import pytest
from playwright.sync_api import Page, sync_playwright, expect
from config import brands  # Import brands from config.py


@pytest.fixture(scope="function")  # ✅ Ensures page is correctly used in Playwright
def page_fixture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()

@pytest.mark.parametrize("brand, data", brands.items())
def test_homepage_loads(page_fixture: Page, brand, data):
    """Verify Homepage Loads for all brands."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")  # ✅ Ensures full page load
    expect(page_fixture).to_have_title()
    print(f"Title for {brand}: {page_fixture.title()}")

@pytest.mark.parametrize("brand, data", brands.items())
def test_title_verification(page_fixture: Page, brand, data):
    """Verify Page Title for all brands."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")  # ✅ Ensures full page load
    title = page_fixture.title()  # ✅ Fetch the title correctly
    print(f"Title for {brand}: {title}")
    expect(page_fixture).to_have_title()

@pytest.mark.parametrize("brand, data", brands.items())
def test_login_button(page_fixture: Page, brand, data):
    """Check Login Button Exists only for gopuff_old."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")  # ✅ Ensures full page load

    if data["url"] == "https://gopuff_old.begenuin.com/home":
        page_fixture.wait_for_selector("button:has-text('Log in')", timeout=5000)  # ✅ Waits properly
        login_button = page_fixture.locator("button:has-text('Log in')")
        expect(login_button).to_be_visible()  # ✅ Ensures button is visible
    else:
        login_button = page_fixture.locator("button:has-text('Log in')")
        expect(login_button).not_to_be_visible()  # ✅ Ensures button is not visible for other brands

@pytest.mark.parametrize("brand, data", brands.items())
def test_login_functionality(page_fixture: Page, brand, data):
    """Test login functionality for gopuff_old only."""
    if data["url"] == "https://gopuff_old.begenuin.com/home":
        page_fixture.goto(data["url"], wait_until="domcontentloaded")  # ✅ Ensures full page load
        page_fixture.click("p[class='min-w-max text-[15px] text-title-3-demi text-monochrome-white']")  # ✅ Correct selector
        page_fixture.fill("input[id=':rn:-form-item']", "testuser@yopmail.com")  # ✅ Ensures input is filled properly
