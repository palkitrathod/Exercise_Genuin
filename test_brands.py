#Here i've imported all the necessary packages and framework
import pytest #Its framework
from playwright.sync_api import Page, sync_playwright, expect #represent the browser tab, function to control browser synch, userd for assertion
from config import brands #Import brands from config file


#fixture is use to launch browser before each test
#Scope is used for - new session for each test case
@pytest.fixture(scope="function", params=["chromium"]) #Params for browser usage
def page_fixture(request): #define the fixture function which provide page object for test
    with sync_playwright() as p: #Playwright will get start
        browser = getattr(p, request.param).launch(headless=False) #start the browser in visible mode
        page = browser.new_page() #Open new tab in browser
        yield page
        browser.close() #after every test, browser will get closed


#Case 1 : Verify that home page is loading successfully
@pytest.mark.parametrize("brand, data", brands.items()) #Runs test multiple time, for each brands
def test_homepage_loads(page_fixture: Page, brand, data): #define the function
    """Check if the homepage loads for each brand."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded") #wait for the page to be loaded
    print(f"{brand} - Loaded successfully. Title: {page_fixture.title()}") #print the page title


#Case 2 : Verify that get app button is shown
@pytest.mark.parametrize("brand, data", brands.items()) #it will make sure that test will run for all the brands
def test_get_app_button(page_fixture: Page, brand, data): #define the function
    """Make sure the 'Get App' button is present (if expected)."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded") #wait for the page t be loaded
    get_app_button = page_fixture.locator("//button[contains(text(), 'Get App')]") #find the get app button on page

#Condition : if get app is true -> expect button to be visible, if false -> it assert
    if data["features"]["get_app"]:
        expect(get_app_button).to_be_visible()
        print(f" '{brand}' has the 'Get App' button.")
    else:
        assert not get_app_button.is_visible(), f" '{brand}' shouldn't have a 'Get App' button, but it does!"
        print(f" '{brand}' does NOT have a 'Get App' button.")


#Case 3 : verify that become a creator button is shown
@pytest.mark.parametrize("brand, data", brands.items())
def test_become_creator_option(page_fixture: Page, brand, data):
    """Check if the 'Become a Creator' option is available (if expected)."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded")
    #locating the become creator app button via xpath
    become_creator_option = page_fixture.locator(
        "(//p[@class='w-64 overflow-hidden p-3 text-start text-body-1-bold'])[1]")
#Condition : if true -> button is there, if false -> it does not have button
    if data["features"]["become_creator"]:
        expect(become_creator_option).to_be_visible()
        print(f" '{brand}' has the 'Become a Creator' button.")
    else:
        assert not become_creator_option.is_visible(), f" '{brand}' shouldn't have 'Become a Creator', but it does!"
        print(f" '{brand}' correctly does NOT have 'Become a Creator'.")


#Case 4 : Verify that login button is there
@pytest.mark.parametrize("brand, data", brands.items())
def test_login_button(page_fixture: Page, brand, data): #define the function
    """Check if the login button is present where expected."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded") #wait until page gets load
    #locate the login button
    login_button = page_fixture.locator(
        "(//button[@class='inline-flex items-center justify-center rounded-md transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary-600 after::bg-primary-600 py-2 h-8 gap-2 px-4'])[1]")

#condition : if true -> login button is there, if false -> login button is not there
    if data["features"]["login"]:
        expect(login_button).to_be_visible()
        print(f" '{brand}' has the login button.")
    else:
        assert not login_button.is_visible(), f" '{brand}' shouldn't have a login button, but it does!"
        print(f" '{brand}' correctly does not have a login button.")

# Case 5 : make sure that if login button is there, verify the login functionality
@pytest.mark.parametrize("brand, data", brands.items())
def test_login_functionality(page_fixture: Page, brand, data):
    """Only test login functionality for brands that support it."""
    page_fixture.goto(data["url"], wait_until="domcontentloaded") #wait page gets load

#condition : skip the test if the login is not supported
    if not data["features"]["login"]:
        pytest.skip(f"Skipping login test for '{brand}' (No login feature).")

    # Find and click the login button
    login_button = page_fixture.locator(
        "(//button[@class='inline-flex items-center justify-center rounded-md transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary-600 after::bg-primary-600 py-2 h-8 gap-2 px-4'])[1]")

    try:
        expect(login_button).to_be_visible() #check if button is there
        login_button.click() #if there it will click on the button
        page_fixture.wait_for_timeout(2000) #it will wait for next action
    except:
        pytest.fail(f" Error: Could not find or click login button on '{brand}'.")

    # Enter email in login form
    email_field = page_fixture.locator("//input[@type='email']")

    try:
        expect(email_field).to_be_visible() #check the email field is available or not
        email_field.fill("testuser@yopmail.com") #if find, it will enter the email address
        email_field.press("Enter") #press submit button
        print(f" Login attempt successful for '{brand}'.")
    except:
        pytest.fail(f" Error : Could not find email field on '{brand}'.")
