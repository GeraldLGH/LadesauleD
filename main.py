from playwright.sync_api import sync_playwright
import config

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(config.URL)

        page.fill("#user_login", config.EMAIL)
        page.fill("#user_pass", config.PASSWORD)

        page.press("#user_pass", "Enter")
        page.wait_for_load_state("networkidle")

        page.screenshot(path="login_result.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    run()
