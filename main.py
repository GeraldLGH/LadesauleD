from playwright.sync_api import sync_playwright
from config import load_config

def run():
    config = load_config()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1 Seite öffnen
        page.goto(config["url"])

        # 2 + 3 Login ausfüllen
        page.fill("#user_login", config["email"])
        page.fill("#user_pass", config["password"])

        # 4 Enter
        page.press("#user_pass", "Enter")

        # Warten bis Seite geladen ist
        page.wait_for_load_state("networkidle")

        # 5 Screenshot
        page.screenshot(path="login_result.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    run()
