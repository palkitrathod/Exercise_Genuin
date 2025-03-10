from playwright.sync_api import sync_playwright

# Brand configurations
brands = {
    "begenuin": {
        "url": "https://begenuin.com/home",
        "features": {
            "login": False,
            "get_app": True,
            "become_creator": True
        }
    },
    "shorts_ted": {
        "url": "https://shorts.ted.com/",
        "features": {
            "login": False,
            "get_app": True,
            "become_creator": False
        }
    },
    "gopuff_old": {
        "url": "https://gopuff_old.begenuin.com/home",
        "features": {
            "login": True,
            "get_app": False,
            "become_creator": True
        }
    }
}

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run in visible mode
        page = browser.new_page()

        for brand, data in brands.items():
            print(f"\n🔹 Running tests for {brand} ({data['url']})")

            # Open website
            page.goto(data["url"], wait_until="domcontentloaded")
            print(f" {brand} - Page Title: {page.title()}")

            # Test: Get App Button
            try:
                get_app_button = page.wait_for_selector("//button[contains(text(), 'Get App')]", timeout=5000)
                if data["features"]["get_app"]:
                    print(f" 'Get App' button is present on {brand}")
                else:
                    print(f" ERROR: 'Get App' button should NOT be present on {brand}")
            except:
                if data["features"]["get_app"]:
                    print(f" 'Get App' button is MISSING on {brand}")
                    page.screenshot(path=f"{brand}_missing_get_app.png")
                else:
                    print(f" 'Get App' button is NOT visible on {brand}")

            # Test: Become a Creator Option
            try:
                become_creator_option = page.wait_for_selector("(//p[@class='w-64 overflow-hidden p-3 text-start text-body-1-bold'])[1]", timeout=5000)
                if data["features"]["become_creator"]:
                    print(f" 'Become a Creator' option is present on {brand}")
                else:
                    print(f" ERROR: 'Become a Creator' option should NOT be present on {brand}")
            except:
                if data["features"]["become_creator"]:
                    print(f" 'Become a Creator' option is MISSING on {brand}")
                    #page.screenshot(path=f"{brand}_missing_become_creator.png")
                else:
                    print(f" 'Become a Creator' option is NOT visible on {brand}")

            # Test: Login Button
            try:
                login_button = page.wait_for_selector("(//button[@class='inline-flex items-center justify-center rounded-md transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary-600 after::bg-primary-600 py-2 h-8 gap-2 px-4'])[1]", timeout=5000)
                if data["features"]["login"]:
                    print(f" Login button is presnt on {brand}")
                else:
                    print(f" ERROR: Login button should NOT be present on {brand}")
            except:
                if data["features"]["login"]:
                    print(f" Login button is MISSING on {brand}")
                    page.screenshot(path=f"{brand}_missing_login.png")
                else:
                    print(f" Login button is NOT visible on {brand}")

            # Test: Login Functionality (Only for gopuff_old)
            if data["features"]["login"]:
                print(f"➡ Attempting login for {brand}...")
                try:
                    login_button.click()
                    page.wait_for_timeout(2000)

                    # Find and enter email
                    email_field = page.wait_for_selector("//input[@type='email']", timeout=5000)
                    email_field.fill("testuser@yopmail.com")
                    email_field.press("Enter")
                    print(f" Login form filled and submitted successfully for {brand}")
                except:
                    print(f" ERROR: Could not find login email field on {brand}")
                    page.screenshot(path=f"{brand}_missing_email_field.png")

        browser.close()

# Run tests
run_tests()
