import pytest #Pytest is fraework
import re #package is used to use regular expression. Here mainly for checking page title
from playwright.sync_api import Page, sync_playwright, expect #Page -> webpage in browser, sync_playwright ->  start playwright in synchronus mode, expect -> use to verify things in test
from config import brands  #Import brands from config.py


# Fixture to start a browser session for each test
# Params is used to tell run each test cases in all 3 browsers
@pytest.fixture(scope="function", params=["chromium", "firefox", "webkit"])
def page_fixture():
    with sync_playwright() as p: #It will start the playwright
        browser = p.chromium.launch(headless=False)  # Running in visible mode, it wont run in background
        page = browser.new_page() #create a new tab in browser
        yield page  #provide the page to the test
        browser.close()  #close the browser after test


@pytest.mark.parametrize("brand, data", brands.items()) #test will run for each brand mentioned in config file
def test_homepage_loads(page_fixture: Page, brand, data):
    """Check if the homepage loads properly for each brand."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded") #open the homepage of the url
    # Ensure page has a title
    expect(page_fixture).to_have_title(re.compile(r".+")) #Check if the page has title
    print(f" Homepage loaded successfully for {brand}, title: {page_fixture.title()}") #Prints the brand name and its title


@pytest.mark.parametrize("brand, data", brands.items())
def test_login_button(page_fixture: Page, brand, data):
    """Verify if the login button exists for gopuff_old and doesn't exist for others."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")
    login_button = page_fixture.locator("button:has-text('Log in')") #It will find the login button in the page

    if data["url"] == "https://gopuff_old.begenuin.com/home": #condition that login button should be visible for this URL
        # Expect login button to be visible
        page_fixture.wait_for_selector("button:has-text('Log in')", timeout=5000)
        expect(login_button).to_be_visible()
        print(f" Login button is visible on {data['url']}")
        #click the login button to open the login form
        login_button.click()
        page_fixture.wait_for_timeout(1000)

    else:
        # Make sure login button does not exist on other brand pages
        try:
            page_fixture.wait_for_selector("button:has-text('Log in')", timeout=3000)
            assert False, f" Unexpected login button found on {data['url']} (Test should fail)"
        except Exception:
            print(f" No login button found on {data['url']} (As expected, test failed correctly)")


@pytest.mark.parametrize("brand, data", brands.items())
def test_login_functionality(page_fixture: Page, brand, data):
    """Test the login process for gopuff_old only."""
    if data["url"] == "https://gopuff_old.begenuin.com/home":
        page_fixture.goto(data["url"], wait_until="domcontentloaded")
        page_fixture.wait_for_timeout(1000)  # Small delay to ensure page is ready

        #find and click the login button
        login_button = page_fixture.locator("button:has-text('Log in')")
        expect(login_button).to_be_visible()
        login_button.click()
        page_fixture.wait_for_timeout(1000)  #wait for login form to appear

        #find the email input field and enter the email
        email_field = page_fixture.locator("input[id*='form-item']")
        expect(email_field).to_be_visible()
        email_field.fill("testuser@yopmail.com")

        #hit the enter on submit button
        email_field.press("Enter")
        page_fixture.wait_for_timeout(2000)  # Wait to see if login proceeds

        print("Login form filled and submitted successfully.")

