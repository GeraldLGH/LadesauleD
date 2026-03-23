import os
from playwright.sync_api import sync_playwright

URL = "https://duesseldorf.ergoladesaeulen.de/wp-login.php?redirect_to=%2F"

EMAIL = os.getenv("LOGIN_EMAIL")
PASSWORD = os.getenv("LOGIN_PASSWORD")

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)

        page.fill("#user_login", EMAIL)
        page.fill("#user_pass", PASSWORD)

        page.press("#user_pass", "Enter")
        page.wait_for_load_state("networkidle")

        page.screenshot(path="login_result.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    run()
